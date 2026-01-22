### Agent2

#### Short Description
Agent2 is a minimal Agent that can execute bash commands. This is a concept, no code exists, just my thoughts of an Agent!

#### Introduction
Agent2 is a program that lets an LLM (Large Language Model) control a Linux machine by executing bash commands. Agent2 controls a machine by writing bash commands at the end of its response. The program will then execute the commands and pipe back the output/error to the LLM. Agent2 tries to be minimalistic and only focus on essentials working things.

Agent2 has no built-in tools. It relies on the host's CLI environment. Therefore, to ensure Agent2 is productive, provide it with the relevant CLI tools and update the agent's preprompt so it knows how to utilize the tools. A great toolkit is **ATK**, it's a standardized toolkit for agentic tasks for general-purpose workflows.

Agent2 is compatible with major LLM providers like OpenRouter (all models), Anthropic (Claude), xAI (Grok), Google (Gemini), and others. It is similar to Claude Code or Agent Zero but minimalistic.

> "A human can do a lot with a terminal, therefore, a terminal agent can do it as well."

Agent2 is programmed in C and is Open-source.

#### Setup / Examples
Here are some common commands to setup Agent2:

```bash
# There is already a prebuild example agent called "example" to make starting easy.
# To launch it write:
agent2 -target "example"

# Create a new agent
# You can setup different agents by giving them a different name
agent2 -create "my_agent"

# Target an Agent (persist until target is changed)
# All subsequent settings will apply to this agent
agent2 -target "my_agent"

# Enter a API-key
agent2 -api_key "API-KEY"

# Set a provider
# Eg "https://openrouter.ai/api/v1/chat/completions" for openrouter
agent2 -provider "your_provider"

# Choose a model
agent2 -model "anthropic/claude-3.5-sonnet"

# Adjust model temperature
agent2 -temperature 0.8

# Start Agent2 with a predefined prompt
agent2 -prompt "what is the meaning of life?"

# Limit the agents tokens / costs (if it ever goes rogue):
# write "nolimit" for unlimited tokens
agent2 -max_tokens 2000

# Launch an Agent2 agent with minimal settings:
agent2 -target "my_agent" -max_tokens 2000 -model "anthropic/claude-3.5-sonnet" -prompt "return the sum of 34+45"
```

#### What Agent2 is Not
*   **No built-in tools:** Bash is enough. If a tool is necessary, it is a separate program that needs to be installed and added to the preprompt to make the model aware. This keeps Agent2 modular and minimalistic.
*   **No fixed agent structure:** Deciding which agent to spawn is up to the agent itself. Guidance can be given in the preprompt.
*   **No GUI overhead.**
*   **No guardrails:** Linux offers lots of tools to restrict a user.
*   **No memory / No RAG:** Not an essential feature.
*   **No MCP integration:** A CLI tool exists for this called `mcp-cli`.
*   **No Multi-modal:** CLI tools can handle this (e.g., `python-llm`, `aichat`, `curl`).

#### Environment
Because Agent2 is a CLI tool, the agent doesn't care if it runs directly on your local machine or in an environment like Docker or Podman.

#### Protocol
The communication protocol between the LLM and host is kept simple: to execute a command, the LLM wraps the command in special words `agent2_command_start` and `agent2_command_end` at the end of its response. The program will then execute the command and pipe back the output/error to the LLM.

#### CLI Interface
*   The agent responds with a blue `AGENT:\n`.
*   The user can input after an orange `USER:\n`.
*   If the model doesn't request a command, the USER is prompted.
*   The user can finish its input with `Ctrl+D` (Standard Unix "end of input").
*   `Enter` will print a normal new line.
*   To interrupt/stop the agent, use `Ctrl+C`.

#### Example Conversation
Here is an example of a USER-AGENT-SYSTEM conversation:

**USER:**
You are Agent2, an Agent that can execute bash commands by wrapping them with `agent2_command_start` and `agent2_command_end` at the end of your prompt. You can ask for user input with the cat bash function. Here is a list of useful programs: ls, cd, curl... list current files!

**AGENT:**
agent2_command_start
ls
agent2_command_end

**SYSTEM:**
boot etc lib run...

**AGENT:**
These are the entries in the current directory:
boot etc lib run...

Conversations are saved under `Agent2/conversation`.

#### Project Directory Structure
Here is the directory structure of Agent2:

```text
agent2/
├── agent2              # Global bash wrapper script
├── bin/                # Compiled binaries
│   └── agent2          # The production C executable
├── config/             # Persistent data
│   ├── program         # Main application settings
│   └── agents/         # Agent-specific profiles
│       ├── example     # Example agent
│       └── my_agent    # User-defined profile
├── conversation/       # Conversation history 
│   ├── 251101_104950   # Conversation (YYMMDD_HHMMSS)
│   └── 251101_104840   # Another conversation
└── dev/                # Source & Build
    ├── agent2.c        # Core logic
    └── compile.sh      # compile
```
