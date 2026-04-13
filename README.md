# LangChain ReAct Agent — First Principles Build

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A minimal LLM agent built from scratch with LangChain and LangGraph to understand how AI agents work. This project implements the **ReAct (Reasoning + Acting) pattern**: an LLM that reasons about a user query, calls external tools to gather information or perform computation, and loops until it can deliver a grounded answer.

## Overview

The agent receives a natural language question and enters a loop:

1. The LLM reads the query and all prior context (conversation history, previous tool results)
2. It decides whether to call a tool or give a final answer
3. If it calls a tool, the framework executes it and feeds the result back to the LLM
4. The loop repeats until the LLM has enough information to respond

```
         ┌──────────────────────────┐
         │                          │
         ▼                          │
   ┌───────────┐   tool call   ┌───────┐
──►│ call_model ├─────────────►│ tools │
   └─────┬─────┘               └───────┘
         │
         │ final answer
         ▼
       OUTPUT
```

## Features

- **ReAct pattern** — The LLM alternates between reasoning and acting, choosing tools based on what information it still needs
- **Tool binding** — Tools are Python functions with descriptions that the LLM reads to decide when and how to use them — the LLM never sees the implementation, only the interface
- **Stateless loop with growing context** — Every LLM call receives the full conversation history because LLMs have no memory between API calls; the message list *is* the agent's memory
- **LLM as decision-maker** — The loop ends not because tools run out, but because the LLM decides it has enough information to answer

### Available Tools

| Tool | Purpose |
|------|---------|
| `wikipedia` | Searches Wikipedia for factual information |
| `multiply` | Multiplies two numbers |
| `add` | Adds two numbers |

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python | Industry standard for ML |
| Agent Framework | LangGraph | Explicit state management, ReAct loop as a state machine |
| LLM Wrappers | LangChain | Model wrappers, tool abstractions, prompt formatting |
| LLM | Claude (Anthropic) | Strong reasoning and tool-calling capabilities |
| Knowledge Source | Wikipedia API | External factual information retrieval |

## Example

```
Ask the agent something: What is 7 times the population of Rome?

Agent flow:
  1. Calls Wikipedia → retrieves Rome's population (2.7 million)
  2. Calls multiply(2700000, 7) → gets 18900000
  3. Returns: "7 times the population of Rome is 18.9 million."
```

## Project Structure

```
My-First-Agent/
│
├── agent.py        # The complete ReAct agent
├── test_setup.py   # Verifies API connection
├── .env.example        # Template for API key setup
├── .env            # API key (not committed)
├── .gitignore
├── Interactive Questions Examples.txt
├── Prompt Output.png
├── requirements.txt    # Python dependencies
└── README.md
```

## How to Run

### Prerequisites

- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup

```bash
# Clone the repository
git clone https://github.com/Massi99RM/My-First-Agent.git
cd My-First-Agent

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
# Copy .env.example to .env and add your key
cp .env.example .env
# Then edit .env and replace the placeholder with your actual key
```

### Run the Agent

```bash
python agent.py
```

## What I Learned

This project was my first step into LLM agents. Key takeaways:

- An agent is fundamentally a **loop with an LLM as the decision-maker** — structurally similar to a reinforcement learning agent's observe-act-observe cycle
- The framework (LangGraph) handles orchestration, the LLM handles reasoning, the tools handle execution — knowing which layer a problem lives in is essential for debugging
- Tool design matters: verbose tool outputs increase cost and consume context window space across every subsequent API call in the loop
- The LLM trusts tool results — it cannot verify them, so tool reliability is an engineering responsibility

## License

MIT