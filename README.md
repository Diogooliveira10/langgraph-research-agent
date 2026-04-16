# 🤖 LangGraph Research Agent – Stateful AI Agent with Web Search

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai)
![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-green?style=flat-square)
![Tavily](https://img.shields.io/badge/Search-Tavily-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## 🧠 Overview

This project implements a **stateful AI research agent** using [LangGraph](https://github.com/langchain-ai/langgraph) and [Tavily Search](https://tavily.com/), capable of autonomously deciding when and how to search the web to answer user queries.

The agent operates on a **LLM → Tool Call → Observation → LLM** execution cycle, managed through a compiled state graph. It supports parallel tool calls, multi-turn reasoning, and graceful fallback when tools are unavailable — all without manual orchestration logic.

- Custom `Agent` class wrapping a `StateGraph` with conditional routing
- Real-time web search via Tavily, triggered only when the model determines it is necessary
- Modular architecture: agent logic, tool setup, and entry point are fully separated
- System prompt externalized to `config.yaml` — behavior tunable without touching code
- Environment-driven configuration via `.env` for API keys, model name, and search parameters

> 💡 While developed in an academic context, every architectural decision here reflects production habits — explicit state management, separation of concerns, configurable limits, and clean interfaces designed to scale.

---

## 🚀 Objective

Build a production-grade research agent using LangGraph's graph primitives to understand how:

- State flows between nodes in a directed graph
- An LLM decides autonomously when to invoke external tools
- Parallel tool calls are handled and results are merged back into conversation state
- Agent behavior can be tuned through configuration rather than code changes

---

## 🎯 Key Features

### 🔄 LangGraph State Machine

- `StateGraph` with two nodes: `llm` (reasoning) and `action` (tool execution)
- Conditional edge routing: if the model returns tool calls → execute; otherwise → end
- Compiled graph ensures deterministic, inspectable execution flow

### 🌐 Real-Time Web Search

- Powered by **Tavily Search API**, returning up to N results per query (configurable via `.env`)
- Supports parallel tool calls — the model can fire multiple searches simultaneously
- Invalid tool names are caught and returned as feedback to the model for self-correction

### 🧩 Modular Architecture

| File          | Responsibility                                      |
| ------------- | --------------------------------------------------- |
| `agent.py`    | `Agent` class, `AgentState`, graph construction     |
| `tools.py`    | Tool instantiation, driven by environment variables |
| `main.py`     | Entry point, model setup, query execution           |
| `config.yaml` | System prompt — editable without touching code      |

### ⚙️ Environment-Driven Configuration

All runtime parameters live in `.env`:

```env
OPENAI_API_KEY=...
OPENAI_BASE_URL=...       # supports OpenRouter or direct OpenAI
TAVILY_API_KEY=...
MODEL_NAME=gpt-4o-mini    # swap models without changing code
TAVILY_MAX_RESULTS=3
```

---

## 🏗️ Architecture

```text
User Query (natural language)
        ↓
main.py → Agent.__init__() → StateGraph compiled
        ↓
Node: llm — GPT-4o-mini reasons and optionally emits tool_calls
        ↓
Conditional Edge — tool_calls present?
    ├── YES → Node: action — Tavily executes search(es)
    │              ↓
    │         ToolMessage injected back into state
    │              ↓
    │         Back to Node: llm
    └── NO  → END — final answer returned
```

---

## 🛠️ Tech Stack

| Layer       | Technology         | Role                                              |
| ----------- | ------------------ | ------------------------------------------------- |
| Language    | Python 3.11+       | Application foundation                            |
| Agent Graph | LangGraph          | Stateful execution graph with conditional routing |
| LLM         | OpenAI gpt-4o-mini | Reasoning, tool call decisions, final answers     |
| Search      | Tavily Search API  | Real-time web search tool                         |
| LLM Client  | LangChain OpenAI   | Model binding and tool registration               |
| Config      | PyYAML             | External system prompt management                 |
| Env         | python-dotenv      | Secure credential and parameter management        |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API key (or OpenRouter)
- Tavily API key — free tier at [app.tavily.com](https://app.tavily.com)

### 1. Clone and set up the environment

```bash
git clone https://github.com/Diogooliveira10/langgraph-research-agent
cd langgraph-research-agent

python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 4. Run the agent

```bash
python main.py
```

---

## 🧪 Test Scenarios

The script ships with two ready-made queries that exercise different reasoning paths:

```
Q: "What is the weather in Rio de Janeiro?"
→ Single tool call to Tavily, real-time weather data returned and summarized

Q: "Who won the 2022 World Cup? What is the GDP of that country?"
→ Parallel tool calls: model fires two searches simultaneously,
  merges results, and answers both questions in a single response
```

---

## 📂 Project Structure

```
.
├── agent.py        # Agent class, AgentState, StateGraph construction
├── tools.py        # Tool instantiation (Tavily Search)
├── main.py         # Entry point, model config, query runner
├── config.yaml     # System prompt — behavior config without code changes
├── requirements.txt
├── .env.example    # Environment variable template
├── .env            # Local credentials (not committed)
└── .gitignore
```

---

## 🎓 Academic Context

This project was developed as part of the:

- 🎓 **Formação em Inteligência Artificial**
- 📍 Offered by **Instituto ECOA PUC-Rio** in partnership with **Serratec**

It corresponds to a hands-on activity from:

- 📌 **Módulo 1 – Construindo Agentes Inteligentes com IA**
- 🧪 **Aula 4 – Fluxo com LangGraph e ferramentas externas**

---

## 👨‍💻 Author

Developed by **Diogo Oliveira**

💼 Full Stack Developer | AI & LLM Enthusiast

Building intelligent systems with LLMs, agent architectures, and modern AI frameworks.

🔗 [LinkedIn](https://www.linkedin.com/in/diiogo-oliveira-dev/) |
💻 [GitHub](https://github.com/Diogooliveira10)

---

## 🧠 Final Notes

This project demonstrates:

- Practical understanding of **stateful agent design** using LangGraph's graph primitives — not just wiring pre-built components, but knowing why each node and edge exists
- Clean separation between **reasoning (LLM)** and **execution (tools)**, making the agent's behavior transparent and testable
- Production habits applied to an academic project: modular structure, environment-driven config, externalized prompts, and explicit error handling
- Hands-on experience with **real-time data retrieval** integrated into an LLM reasoning loop

> 🚀 Understanding how a graph-based agent routes state, handles tool calls, and loops back into reasoning is what separates engineers who use AI frameworks from those who understand them. That distinction is what this project was built to develop.
