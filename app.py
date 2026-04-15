from dotenv import load_dotenv
import os
_ = load_dotenv()
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=3)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # verificar nome de ferramenta incorreto do LLM
                print("\n ....incorrect tool name....")
                result = "Incorrect tool name, try again"  # instruir LLM a tentar novamente
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
    
prompt = """
You are an intelligent research assistant. Use the search engine to look for information. \
You can make multiple calls (together or in sequence). \
Only search for information when you are sure of what you need. \
If you need to look up some information before asking a follow-up question, you can do that!
"""

model = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL")
)
abot = Agent(model, [tool], system=prompt)

messages = [HumanMessage(content="What is the weather in Rio de Janeiro?")]
result = abot.graph.invoke({"messages": messages})
print("Full result:")
print(result)
print("\nFinal answer:")
print(result['messages'][-1].content)

query = "Who won the 2022 World Cup? What is the GDP of that country? Answer each question." 
messages = [HumanMessage(content=query)]
abot = Agent(model, [tool], system=prompt)
result = abot.graph.invoke({"messages": messages})
print(result['messages'][-1].content)
