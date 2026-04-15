import operator
from typing import Annotated
from typing import TypedDict

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools: list, system: str = ""):
        self.system = system

        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END},
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")

        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState) -> bool:
        """Verifica se o modelo solicitou chamada de alguma ferramenta."""
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState) -> dict:
        """Chama o modelo LLM com o histórico de mensagens."""
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {"messages": [message]}

    def take_action(self, state: AgentState) -> dict:
        """Executa as ferramentas solicitadas pelo modelo."""
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if t["name"] not in self.tools:
                print("  ....incorrect tool name....")
                result = "Incorrect tool name, try again"
            else:
                result = self.tools[t["name"]].invoke(t["args"])
            results.append(
                ToolMessage(
                    tool_call_id=t["id"],
                    name=t["name"],
                    content=str(result),
                )
            )
        print("Back to the model!")
        return {"messages": results}
