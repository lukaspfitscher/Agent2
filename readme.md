# Agent2
A lightweight Agent that can execute scripts
## Introduction
```text
Agent2 is a program that lets an LLM (Large language model)
control a linux machine by writing/executing a bash script.

Agent2 controls a machine by writing a bash script at the end of its response.
The script will be extractet from response of the LLM, executed and the output/error will be piped back to the LLM.

Agent2 tries to be minimalistic and focuses on essentials.

Agent2 has no built-in tools and therefore relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agents `context` so it knows how to utilize these tools.

Under the "Useful software" section, there is a list of 
useful CLI tools to make Agent2 productiv for general purpose workflows

Agent2 is compatible nearly all LLM providers:
Openrouter (all models), Anthropic (Claude), xAI (Grok), Google (Gemini) ...

Agent2 is similar to Claude Code or Agent Zero but lightweight.

```
> [!QUOTE]
> A human can do a lot with a script/terminal, therefore, a agent can do it as well
> The more agents/LLM advance the less of a framework is required
> Agent2 is an Agent framework for Agents

```text
Agent2 is programmed by Lukas Pfitscher in `Python`, Linux only and Open-source
```
## Setup / Examples
```text
- Only `python`, `request` and `json` are reqired to run Agent2.
- To install these libraries execute `install.sh`
```
## What Agent2 is not
- No built-in tools:
    With Bash the agent can use all installed CLI tools,
    if an additional tool is required, it needs to be installed and
    added to the LLMs context to make the LLM aware of the tool.
    This keeps Agent2 minimalistic and modular.
- No fixed agent structure:
    Deciding which agent to spawn is up to the agent itself.
    More about thie is in the "Multi agent support" secion
    Guidance can be given in the model context
- CLI interfce only: No GUI overhead
- No guardrails: 
    This is done be user restriction and environments (docker, podman...).
    Linux offers lots of tools to restrict a user.
- No MCP integration: a CLI tool exists for this "`mcp-cli`"
- No Multi-modal: CLI tools can handle this: `python-llm`,`aichat`,`curl`
- No memory / No RAG: not an essential feature
## Environment
- Because Agent2 is a CLI tool it can run directly on 
  your local machine, server or in an environment(docker, podman...).
## Protocol overview
- The file `context.txt` contains the context of the model, like "You are Agent2, a..."
- The user can input after a `USER:`
- For user input, the Enter key is a normal new line,
  submit with Ctrl+D (standard Unix convention for 'end of input')
- The LLM responds with `AGENT:` 
- The communication between LLM and SYSTEM is kept simple:
  The LLM triggers script execution by wrapping the script text around
  `agent2_script_start+enter` and `enter+agent2_script_end` at the end of its response.
- After that the script gets executed in a seperate shell. It doesnt block the agent.
- The script output is written to the file called `output.txt`.
- Agent2 waits 0.5 seconds for the command to finish and produce an output.
- The output/error is piped back to the LLM after`SYSTEM:` message.
- If the command takes longer Agent2 can but itself into sleep with his PID
- Conversations are saved as plain text 
  under `conversation.txt`
- If the model doesn't request another script the user is promped.
- The user can stop agent2 by pressing ctrl+c

## Example conversation
Here is an example of a minimal USER-AGENT-SYSTEM conversation:

`USER:`
You are Agent2, an Agent that can execute bash scripts
by wrapping them with agent2_script_start and agent2_script_end
at the end of its responds. 

Here is a list of useful programs: ls, cd, curl...
list current files!

You need handel evert terminal input youself
for example to do `ls` you need to write `ls` you need to write als enter like this `ls\n`

You can wait for a certain time by writing `agent2_wait time_in_sec` at the end of your respons
For example the user requests to wait for a certain time or to wait for a program to finish

`LLM:`
agent2_script_start
ls
agent2_script_end

`SYSTEM:`
boot etc lib run...

`LLM:`
These are the entries in the current directory:
boot etc lib run...

## Project directory structure
Here is the directory structure of Agent2:

```text
agent2/
├─ readme.md          # Documentaion (the file you are currently reading)
├─ agent2.py          # Single python file (whole code)
├─ instal.sh          # Instalation
├─ config.py          # Contains api key, provider
├─ prompt.txt         # Containing the Prompt
├─ context.txt        # Context of the model
├─ conversation.txt   # File where conversation is saved
├─ script.sh          # Script that agent can write to and exectute
├─ output.txt         # Output and error
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

## Multi agent support
- To make new agents make a copy of Agent2 directory
- We keep this simple: one program, one agent, one conversation
- Integrating multiagent directly in the program makes everthing much more complex
### To create a new agent:
```bash
# Copy current agent
cp path_agent_dir path_new_agent_dir

# move to the new agent dir
cd path_new_agent_dir

# Optionally remove existing conversations
rm conversation.txt

# Add a prompt to the model by writing to the prompt file
echo "You are a subagent, make a cleanup of..." > prompt

# Launch an Agent2:
python3 agent2.py
```
Agent2 can do this by itself just prompt it right.

## Q&A

### Why not using a psydo terminal
Handling all the controll sequences gets to complicatet.
Just writing to a files and executing is much simpler
and the agent can do already a lot.

### What if i want to turn the agent into sleep
Agent2 also gives the LLM its PID and can therefore but itself into sleep with
kill -STOP <PID> && sleep 10 && kill -CONT <PID>

### Chat tempalates




















