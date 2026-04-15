import os
from langchain_tavily import TavilySearch


def get_tools() -> list:
    """Retorna a lista de ferramentas disponíveis para o agente."""
    max_results = int(os.getenv("TAVILY_MAX_RESULTS", 3))
    search_tool = TavilySearch(max_results=max_results)
    return [search_tool]