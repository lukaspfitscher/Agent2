# Agent2

A lightweight agent that controls your computer by executing Bash scripts

## Introduction

- Agent2 is a program that lets an LLM (Large language model)
control a linux machine by writing/executing a bash script.

- Agent2 controls a machine by writing a bash script at the end of its response.
The script will be extractet from response of the LLM, executed and the output/error will be piped back to the LLM.

- Agent2 tries to be minimalistic and focuses on essentials.

- Agent2 has no built-in tools and therefore relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agents `context` so it knows how to utilize these tools.

- Under the "Useful software" section, there is a list of 
useful CLI tools to make Agent2 productive for general purpose workflows

- Agent2 is compatible with nearly all LLM providers:
OpenRouter (all models), Anthropic (Claude), xAI (Grok), Google (Gemini) ...

- The goal is not security or production-readiness; it is to be minimalistic, easy to understand, and easy to extend.

- With only ~130 lines of Python code Agent2 is short, very light and still quite capable.

- Agent2 is similar to Claude Code or Agent Zero but lightweight.

> [!QUOTE]
> A human can do a lot with a script/terminal, therefore, an agent can do it as well
> The more agents/LLMs advance the less of a framework is required
> Agent2 is an Agent framework for Agents

```text
Agent2 is programmed in `Python`, Linux only and Open-source on [Github](https://github.com/lukaspfitscher/Agent2) written by Lukas Pfitscher 
```

## Quick setup
- Only `python` and the `request` library are required to run Agent2.
- To install these libraries go into the agent directory and execute `./install.sh`
- or just past this in your terminal `apt update; apt install -y python3 python3-pip python3-requests`.
- Add your Openrouter API key in the config.py file.
- launch the Agent2 with `python3 agent2.py` (Be careful! Use an environment!)

## What Agent2 is not
- No built-in tools:
    With Bash the agent can use all installed CLI tools,
    if an additional tool is required, it needs to be installed and
    added to the LLMs context to make the LLM aware of the tool.
    This keeps Agent2 minimalistic and modular.
- No fixed agent structure:
    Deciding which agent to spawn is up to the agent itself.
    More about this is in the "Multi agent support" section.
- CLI interface only: No GUI overhead
- No guardrails: 
    This is done by user restriction and environments (docker, podman...).
    Linux offers lots of tools to restrict a user.
- No MCP integration: a CLI tool exists for this "`mcp-cli`"
- No Multi-modal: a simple script can handle this: `python-llm`,`aichat`,`curl`
- No memory / No RAG: not an essential feature

## Environment

- Because Agent2 is a CLI tool it can run directly on 
  your local machine, server, VPS or in an environment(docker, podman...).

## Protocol overview

- The file `context.txt` contains the context of the model, like "You are Agent2, a..."
- All whats written is exactly as it sees the LLM in the terminal, except yellow notes
- The user can input after a `USER:`
- For user input, the Enter key is a normal new line,
  submit with Ctrl+D (standard Unix convention for 'end of input')
- The LLM responds with `LLM:` 
- The communication between LLM and SYSTEM is kept simple:
  The LLM triggers script execution by writting: `agent2_script: `
- After that the script gets executed in a seperate shell. 
- It runs in a seperate shell and therefore doesnt block the agent.
- The script output is written to the file called `output.txt`.
- Agent2 waits 2 seconds for the command to finish and produce an output.
- For longer waittimes theagent can put itself into sleep with its PID.
- The output/error is piped back to the LLM after`TOOL:` message.
- If the command takes longer, Agent2 can put itself into sleep with its PID.
- Conversations are saved as plain text (no json) in `conversation.txt`.
- In the conversation the text is exactly as the model sees it.
- The conversation includes all the start and stop markers.
- If the model doesn't request another script, the user is prompted.
- The user can stop agent2 by pressing ctrl+c

## Example conversation

Here is an example of a minimal USER-AGENT-SYSTEM conversation:

`USER:`
You are Agent2, an Agent that can execute bash scripts
by writting `agent2_script: `

Here is a list of useful programs: ls, cd, curl...
list current files!

You need handel evert terminal input youself
for example to do `ls` you need to write `ls` you need to write als enter like this `ls\n`

For example the user requests to wait for a certain time or to wait for a program to finish

`LLM:`
agent2_script: ls

`TOOL:`
boot etc lib run...

`LLM:`
These are the entries in the current directory:
boot etc lib run...

## Project directory structure

Here is the directory structure of Agent2:

```text
agent2/
├─ working_dir/       # The directory where the script is executed.
├─ readme.md          # Documentation (the file you are currently reading)
├─ agent2.py          # Single python file (whole code)
├─ install.sh         # Instalation script
├─ config.py          # Contains api key, provider
├─ prompt.txt         # Containing the Prompt
├─ context.txt        # Context of the model
├─ conversation.txt   # File where conversation is saved
├─ script.sh          # Script that agent can write to and exectute
├─ output.txt         # Output and error of the script
```

## Useful software

Agent2 comes with no software. Here is an example how to give Agent2 internet search capabilities.

First install the software as usual:

```Bash
apt install -y ddgr #Get raw website content
apt install -y curl #Retrieve web search results (`ddgr -x`)
apt install -y lynx #Extract useful text (`curl -s https://www.x.com | lynx -stdin -dump`)
```

Add a note to `context.txt` so the model knows it can use these tools like this:
```text
You can search the web with ddgr, curl, lynx
```

## Multi agent support

- To make new agents make a copy of Agent2 directory
- Guidance can be given in the model context
- We keep this simple: one program, one agent, one conversation
- Integrating multiagent directly in the program makes everthing much more complex

### Create a new agent

```bash
# Copy current agent
cp path_agent_dir path_new_agent_dir

# move in to the new agent dir
cd path_new_agent_dir

# Optionally remove existing conversation
rm conversation.txt

# Add a prompt to the model by writing to the prompt file
echo "You are a subagent, make a cleanup of..." > prompt

# Launch Agent2:
python3 agent2.py
```
Agent2 can do this by itself just prompt it right.

## Q&A and unsorted notes

### Why not using a pseudo terminal?
Handling all the controll sequences gets to complicatet.
Just writing to a files and executing is much simpler.
With this the agent can do already a lot. It doesnt need a pseudo terminal.

### What if i want to turn the agent into sleep?
Agent2 also gives the LLM its PID and can therefore but itself into sleep with
kill -STOP <PID> && sleep 10 && kill -CONT <PID>

### Chat tempalates
Just writing `user:` or `system:` wont work.
Every model needs a specific chat format.
Without this format the model behaves terrible!
The correctness of stop tokens and role markers is crucial for stable behavior.
If you change a model you also need to change these Marker under config.py.
You can look them up on the internat for each model.

### Would it be great to also give the LLM the PID of the script?
The script can do this by iteself by adding `echo "Shell PID: $$"`.
For most commands this is not needed becasue they will finish and the shell close automaticly.

### Will it work for other non debian based distros like arch?
Yes, just change the content of `install.sh` to you distros installer.
Everthing else stays the same.