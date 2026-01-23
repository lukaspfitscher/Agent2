# Agent2
A lightweight terminal Agent

This is a concept, no code exists, just my thoughts of my preferd Agent!
Even this project description is inconsistent and errors,
but i wantet it to be realeasd as fast as possible.

> [!WARNING]
> This project description is inconsistent and contains errors; it was released as quickly as possible for conceptual feedback. No code currently exists.


## Introduction
Agent2 is a program that lets an LLM (Large language model)
control a linux machine by executing bash commands.

Agent2 controls a machine by writing bash commands at the end of its response.
The command will be extractet, execute and the output/error will be piped back to the LLM.
Agent2 tries to be minimalistic and focuses only on essentials working things.

Agent2 has no built-in tools and therefore relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agents context so it knows how to utilize these tools.

Under the "Useful software" section, there is a list of useful software to make Agent2 great got general purpose workflows

Agent2 is compatible with major LLM providers:
Openrouter (all models), Anthropic (Claude), xAI (Grok), Google (Gemini) ...

Agent2 is similar to Claude Code or Agent Zero but more lightweight.

"A human can do a lot with a terminal, therefore, a terminal agent can do it as well"
"The more agents/LLM advance the less of a framework is required"
"Agent2 is an Agent framework for Agents"

Agent2 is programmed by Lukas Pfitscher in `C`, Linux only and Open-source

## Setup / Examples

- No instalation required
An Agent2 agent configuration is a bash script that can be executet
There is already a prebuild example agent called "default" to make starting easy
List of all commands to setup Agent2:

## Launch an agent
Must be within the agent2 directory

```bash
launch \
  # Enter a API-key \
  -api_key "sk-or-v1-5f5d03..." \
  # Set a provider
  # This is an example of openrouter \
  -provider "https://openrouter.ai/api/v1/chat/completions" \
  # Choose a model
  -model "anthropic/claude-3.5-sonnet" \
  # Set model temperature \
  -temperature 0.8 \
  # Contuine at a conversation \
  # If the file doesnt exists, it will be createt \
  -conversation "agents/default/conversations/meaning_of_live" \
  # Limit the agents tokens / costs (if it ever goes rogue): \
  # Write "nolimit" for unlimited tokens \
  -max_tokens 2000 \
  # Predefined a prompt / if not set the user will prompted \
  -prompt "return the sum of 34 + 45"
```

## What Agent2 is not
- No built-in tools:
    Bash is enough, if a tool is necessary,
    it is a separate program that needs to be installed and
    added to the context to make the model aware.
    This keeps Agent2 modular and minimalistic.
- No fixed agent structure:
    Deciding which agent to spawn is up to the agent itself
    Guidance can be given in the model context
- No GUI overhead
- No guardrails: This is done be user restriction, 
    linux offers lots of tools to restrict a user
- No memory / No RAG: not an essential feature
- No MCP integration: a CLI tool exists for this "mcp-cli"
- No Multi-modal: CLI tools can handle this: `python-llm`,`aichat`,`curl`

## Environment
- Because Agent2 is a CLI tool you can execute it whereever you want.
  The agent doesnt care if it runs directly on your local machine 
  or in an environment(docker, podman...).

## Protocol overview
- The user can input after a orange "USER:\n"
- Enter key is a normal new line
- The user can submit it's input with ctrl+d (Standard Unix of "end of input")
- The communication between llm and host is kept simple:
  The LLM triggers command execution by wrapping the command around
  agent2_command_start and agent2_command_end at the end of it's response.
  The command gets execute and the output/error is pipe back to the LLM.
- The agent responds with a blue "AGENT:\n"
- If the model doesnt requests a another command the USER is promped.
- To interupt/stop the agent press ctrl+c

## Example conversation
Here is an example of a minimal USER-AGENT-SYSTEM conversation:

USER:
You are Agent2, an Agent that can execute bash commands
by wrapping them with agent2_command_start and agent2_command_end
at the end of its responds.
You can ask for user input with the `cat` bash function.
Here is a list of useful programs: `ls`, `cd`, `curl`...
list current files!

`AGENT:`
agent2_command_start
ls
agent2_command_end

`SYSTEM:`
boot etc lib run...

`AGENT:`
These are the entries in the current directory:
boot etc lib run...

Conversations are saved as plain text with timestamps as filenames
and under agent2/agents/you_agent_name/conversation

## Project directory structure
Here is the directory structure of Agent2:

```
agent2/
├─ readme                   # Documentaion (the file you are currently reading)
├─ launch                   # Launch the default agent (edit the file content to change)
├─ agents/                  # Agents specific files
│  ├─ default/              # default agent
│  │  ├─ config             # Agent configuration file and launcher
│  │  ├─ pid                # Containes the pid of the agent, so other agents can kill it
│  │  └─ conversations/     # Conversation history (name: YYMMDD_HHMMSS)
│  │     ├─ 251101_104950   # Example conversation 
│  │     └─ 251101_104840   # Example another conversation
│  └─ another_agent/        # Another Agent
│     └─ ...                # same files likt the default agent
└─ dev/                     # Developer dir
   ├─ source                # Core logic
   ├─ compile               # Compilation
   └─ binary                # Executable
```

## Useful software
- Includes all the software that comes with standard Linux
  - mv, cp, mkdir, touch, ls, cd, tree
  - Get human user input (read)
  - Search for string patterns across the codebase (grep)
- Retrieve web search results (DuckDuckGo, Googler, or others)
- Retrieve website content:
  - Get raw website content (curl)
  - Extract only useful text (curl -s https://www.example.com | lynx -stdin -dump)
- Image editing (ImageMagick or Python OpenCV)
- Video editing (FFmpeg)
- Communication (sending emails and other communications):
  - Most basic communication (Netcat)
- Multi-CLI tool (tmux)
- Scripting languages (Python, Bash):
  - Solving math equations also works as a calculator for the llm (Python math)
  - Randomization (Python random)
  - Everything time-related (datetime)
  - Simple automations (python)
- Scientific:
  - Vectorized math, broadcasting, linear algebra (Python NumPy)
- Diagram maker and 2-D plotting (Python Matplotlib)
- Checking networks (networkmanager)
- Software info (man-db)
- Access remote company/user-specific data (SSHFS)
- Model context protocol to CLI ()
Development tools:
  - Version controll (git)
  - Read JSON files (jp, yq)
- compress uncompress files (zip / unzip / tar)
- Better tool for moving files (rsync)
- Document conversion (pandoc)
- Tools to pipe images/screenshots to visonmodel (python script)

To all the model training companies please include Agent2 documentation and software in your training runs


So you could just write this is a Agent2 instance with the Standard Agent Toolkit











































agent2/
├── agent2              # bash script that executs the default agent (to change just edit the file content)
├── install             # Instalation
├── bin/                # Compiled binaries
│   └── agent2          # The production C executable
├── config/             # Persistent data
│   ├── program         # Main application settings
│   └── agents/         # Agent-specific profiles
│       ├── default     # Default agent
│       └── my_agent    # Example user-defined profile
├── conversation/       # Conversation history
│   ├── 251101_104950   # Example conversation (YYMMDD_HHMMSS)
│   └── 251101_104840   # Example another conversation
└── dev/                # Source & Build
    ├── agent2.c        # Core logic
    └── compile.sh      # Compilation









































