from dotenv import load_dotenv
import os
import yaml

_ = load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from agent import Agent
from tools import get_tools


def load_config(path: str = "config.yaml") -> dict:
    """Carrega as configurações do arquivo YAML."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_query(query: str, model, tools: list, system_prompt: str) -> str:
    """Cria um agente, executa uma query e retorna a resposta final."""
    abot = Agent(model, tools, system=system_prompt)
    messages = [HumanMessage(content=query)]
    result = abot.graph.invoke({"messages": messages})
    return result["messages"][-1].content


def main():
    config = load_config()
    system_prompt = config["agent"]["system_prompt"]

    model = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
    )
    tools = get_tools()

    # Query 1
    answer = run_query("What is the weather in Rio de Janeiro?", model, tools, system_prompt)
    print("\nFinal answer:")
    print(answer)

    # Query 2
    answer = run_query(
        "Who won the 2022 World Cup? What is the GDP of that country? Answer each question.",
        model,
        tools,
        system_prompt,
    )
    print("\nFinal answer:")
    print(answer)


if __name__ == "__main__":
    main()
