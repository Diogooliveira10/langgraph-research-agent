from dotenv import load_dotenv
import os

_ = load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from agent import Agent
from tools import get_tools


SYSTEM_PROMPT = """
You are an intelligent research assistant. Use the search engine to look for information. \
You can make multiple calls (together or in sequence). \
Only search for information when you are sure of what you need. \
If you need to look up some information before asking a follow-up question, you can do that!
"""


def run_query(query: str, model, tools: list) -> str:
    """Cria um agente, executa uma query e retorna a resposta final."""
    abot = Agent(model, tools, system=SYSTEM_PROMPT)
    messages = [HumanMessage(content=query)]
    result = abot.graph.invoke({"messages": messages})
    return result["messages"][-1].content


def main():
    model = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
    )
    tools = get_tools()

    # Query 1
    answer = run_query("What is the weather in Rio de Janeiro?", model, tools)
    print("\nFinal answer:")
    print(answer)

    # Query 2
    answer = run_query(
        "Who won the 2022 World Cup? What is the GDP of that country? Answer each question.",
        model,
        tools,
    )
    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()
