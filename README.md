# Agent2
A lightweight terminal Agent

> [!WARNING]
> This project description is inconsistent and contains errors; it was released as quickly as possible for conceptual feedback. No code currently exists.
## Introduction
```text
Agent2 is a program that lets an LLM (Large language model)
control a linux machine by executing bash commands.

Agent2 controls a machine by writing bash commands at the end of its response.
The command will be extractet, execute and the output/error will be piped back to the LLM.
Agent2 tries to be minimalistic and focuses only on essentials working things.

Agent2 has no built-in tools and therefore relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agents context so it knows how to utilize these tools.

Under the "Useful software" section,
there is a list of useful software to make Agent2 great for general purpose workflows

Agent2 is compatible with major LLM providers:
Openrouter (all models), Anthropic (Claude), xAI (Grok), Google (Gemini) ...

Agent2 is similar to Claude Code or Agent Zero but more lightweight.
```
> [!QUOTE]
> A human can do a lot with a terminal, therefore, a terminal agent can do it as well
> The more agents/LLM advance the less of a framework is required
> Agent2 is an Agent framework for Agents

```text
Agent2 is programmed by Lukas Pfitscher in `C`, Linux only and Open-source
```
## Setup / Examples
```text
- No instalation required
An Agent2 agent configuration is a bash script that can be executet
There is already a prebuild example agent called "default" to make starting easy
List of all commands to setup Agent2:
```
## Launch an agent
Execute the lauch binary inside the agent2 directory

```bash
./launch
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
    Deciding which agent to spawn is up to the agent itself.
    Guidance can be given in the model context
- CLI interfce only: No GUI overhead
- No guardrails: This is done be user restriction, 
    linux offers lots of tools to restrict a user
- No memory / No RAG: not an essential feature
- No MCP integration: a CLI tool exists for this "`mcp-cli`"
- No Multi-modal: CLI tools can handle this: `python-llm`,`aichat`,`curl`
## Environment
- Because Agent2 is a CLI tool it can runs directly on your local machine 
  or in an environment(docker, podman...).
## Protocol overview
- The user can input after a orange "USER:\n"
- Enter key is a normal new line, submit with ctrl+d (Standard Unix of "end of input")
- The communication between LLM and host is kept simple:
  The LLM triggers command execution by wrapping the command around
  agent2_command_start and agent2_command_end at the end of it's response.
  The command gets execute and the output/error is pipe back to the LLM.
- The agent responds with a blue "AGENT:\n"
- If the model doesnt requests a another command the USER is promped.
- To interupt/stop the agent press ctrl+c
## Example conversation
Here is an example of a minimal USER-AGENT-SYSTEM conversation:

`USER:`
You are Agent2, an Agent that can execute bash commands
by wrapping them with agent2_command_start and agent2_command_end
at the end of its responds. 

Here is a list of useful programs: ls, cd, curl...
list current files!

`AGENT:`
agent2_command_start
ls
agent2_command_end

`SYSTEM:`s
boot etc lib run...

`AGENT:`
These are the entries in the current directory:
boot etc lib run...

Conversations are saved as plain text with timestamps as filenames
under agent2/conversation

## Project directory structure
Here is the directory structure of Agent2:

```text
agent2/
├─ readme             # Documentaion (the file you are currently reading)
├─ launch             # Launch the agent
├─ config             # Contains api key, provider
├─ pid                # Containes the pid of the agent, so other agents can kill it
├─ conversations/     # Conversation history (default name: YYMMDD_HHMMSS)
│  ├─ 251101_104950   # Example conversation
│  └─ what_is_life    # Example another conversation, given a name instead of a timestamp
└─ dev/               # Developer dir
   ├─ source          # Source code
   └─ compile         # Compilation
```

## Useful software

Here is a list of usefull programs of the agent.
We call this the Standard Agent Toolkit - Short ATK:

- Includes all the software that comes with standard Linux
  - `mv`, `cp`, `mkdir`, `touch`, `ls`, `cd`, `tree`
  - Get human user input (`cat`)
  - Search for string patterns across the codebase (`grep`)
- Retrieve web search results (`ddgr -x`)
- Retrieve website content:
  - Get raw website content (`curl`)
  - Extract only useful text (`curl -s https://www.example.com | lynx -stdin -dump`)
- Image editing (`ImageMagick` or Python `OpenCV`)
- Video editing (FFmpeg)
- Communication (sending emails and other communications):
  - Most basic communication (`Netcat`)
- Multi-CLI tool (`tmux`)
- Scripting languages (`Python`):
  - Solving math equations also works as a calculator for the llm (Python math)
  - Randomization (Python `random`)
  - Everything time-related (`datetime`)
  - Simple automations (`python`)
- Scientific:
  - Vectorized math, broadcasting, linear algebra (Python `NumPy`)
- Diagram maker and 2-D plotting (Python `Matplotlib`)
- Checking networks (`networkmanager`)
- Software info (`man-db`)
- Access remote company/user-specific data (`SSHFS`)
- Model context protocol to CLI (`mcp-cli`)
Development tools:
  - Version controll (`git`)
  - Read JSON files (`jp`, `yq`)
- compress uncompress files (`zip` / `unzip` / `tar`)
- Better tool for moving files (`rsync`)
- Document conversion (`pandoc`)
- Tools to pipe images/screenshots to visonmodel (python script)

## program structure

```text
read config settings
if prompt given jump to "LLM ask"
infinite loop (break with ctrl+c)
  go to label no command
  user input, send with ctrl+d
  go to label LLM ask
  LLM ask
  update conversation
  extract command
  if no command go to user input
  execute command
  get error/output
  update conversation
```

## Multi agent support
- To spawn new agents make a copy of Agent2
- We keep this simple: one program, one agent
- Integrating multiagent directly in the program makes everthing much more complex

### To spawn a new agent:
```bash
# Copy current agent
cp path_agent_dir path_new_agent_dir

# Optionally remove existing conversations
rm -rf path_new_agent_dir/conversation/*

# Launch an Agent2 with a preprompt:
cd path_new_agent_dir
./launch -prompt "You are a subagent, make a cleanup of..."
```

### Terminate an Agent
Each agent creates a PID file containing its process ID. To terminate an agent:
```bash
kill $(cat path_new_agent_dir/PID)
```




























