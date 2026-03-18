# LangChain ReAct Agent — First Principles Build

A minimal LLM agent built from scratch with LangChain and LangGraph to understand how AI agents work. This project implements the **ReAct (Reasoning + Acting) pattern**: an LLM that reasons about a user query, calls external tools to gather information or perform computation, and loops until it can deliver a grounded answer.

## How It Works

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

## Available Tools

| Tool | Purpose |
|------|---------|
| `wikipedia` | Searches Wikipedia for factual information |
| `multiply` | Multiplies two numbers |
| `add` | Adds two numbers |

## Example

```
Ask the agent something: What is 7 times the population of Rome?

Agent flow:
  1. Calls Wikipedia → retrieves Rome's population (2.7 million)
  2. Calls multiply(2700000, 7) → gets 18900000
  3. Returns: "7 times the population of Rome is 18.9 million."
```

## Tech Stack

- **Python 3.10+**
- **LangChain** — model wrappers, tool abstractions, prompt formatting
- **LangGraph** — agent orchestration (the ReAct loop as a state machine)
- **Claude (Anthropic API)** — the LLM powering the agent's reasoning
- **Wikipedia API** — external knowledge source

## Setup
 
1. Clone the repository:
```bash
git clone https://github.com/Massi99RM/My-First-Agent.git
cd my-first-agent
```
 
2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
 
3. Install dependencies:
```bash
pip install langchain-anthropic langgraph langchain-community wikipedia python-dotenv
```
 
 4. Create a `.env` file in the project root with your Anthropic API key:
```
ANTHROPIC_API_KEY=your-key-here
```
 
5. Run the agent:
```bash
python agent.py
```

## Key Concepts Demonstrated

- **ReAct pattern**: the LLM alternates between reasoning and acting, choosing tools based on what information it still needs
- **Tool binding**: tools are Python functions with descriptions that the LLM reads to decide when and how to use them — the LLM never sees the implementation, only the interface
- **Stateless loop with growing context**: every LLM call receives the full conversation history because LLMs have no memory between API calls; the message list *is* the agent's memory
- **LLM as decision-maker**: the loop ends not because tools run out, but because the LLM decides it has enough information to answer

## Project Structure

```
my-first-agent/
├── test_setup.py   # Verifies API connection
├── agent.py        # The complete ReAct agent
├── .env            # API key (not committed)
├── .gitignore
└── README.md
└── Interactive Questions Examples   # Other examples
└── Prompt Output.png   # What you see on the console 
```

## What I Learned

This project was my first step into LLM agents. Key takeaways:

- An agent is fundamentally a **loop with an LLM as the decision-maker** — structurally similar to a reinforcement learning agent's observe-act-observe cycle
- The framework (LangGraph) handles orchestration, the LLM handles reasoning, the tools handle execution — knowing which layer a problem lives in is essential for debugging
- Tool design matters: verbose tool outputs increase cost and consume context window space across every subsequent API call in the loop
- The LLM trusts tool results — it cannot verify them, so tool reliability is an engineering responsibility


