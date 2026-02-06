# Agent2

A lightweight agent that controls your computer by executing Bash scripts

## Introduction:

- Agent2 controls a machine by writing a bash script at the end of its response.
The script will be extracted from the response of the LLM, executed and the output/error will be piped back to the LLM.

- Agent2 tries to be minimalistic and focuses on essentials. With only ~130 lines of Python code, Agent2 is short, simple / very light / easy to understand /easy to extend and still quite capable.

- Agent2 relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agents `context.txt` so it knows how to utilize these tools.
Under the "How to add tools" section, there is an example.

> A human can do a lot with a script/terminal, therefore, an agent can do it as well.
> The more agents/LLMs advance the less of a framework is required.
> Because it's so simple, Agent2 is an Agent framework for Agents

Agent2 is programmed in `Python`, Open-source on [Github](https://github.com/lukaspfitscher/Agent2) and written by Lukas Pfitscher

## Quick setup:

- Only `python` and the `requests` library are required to run Agent2.
- To install these libraries, go into the agent2 directory and execute `./install.sh`
- or just paste this in your terminal:
```bash
`apt update; apt install -y python3 python3-pip python3-requests
```
- Next add your Openrouter API key in the agent2.py file.
- Launch Agent2 with `python3 agent2.py` (Be careful! It can control your system! )

## Environment:

- Because Agent2 is a CLI tool it can run directly on 
  your local machine, server, VPS or in an environment(docker, podman...).

## Protocol overview:

- The file `context.txt` contains the context of the model, like "You are Agent2, a..."
- Everything written to the terminal or in the conversation.txt 
  file is exactly as it is seen by the LLM,
  except the yellow notes in the terminal for better visualization.
- The user can input after a `INPUT:`
- For user input, the Enter key is a normal new line,
  submit with Ctrl+D (standard Unix convention for 'end of input')
- The LLM responds with `LLM:` 
- The communication between LLM and SYSTEM is kept simple:
  The LLM triggers script execution by writing: `agent2_script: `
- After that the script gets executed in a separate shell and therefore doesn't block the agent.
- The script output is written to the file called `output.txt`.
- Agent2 waits 0.2 seconds for the command to finish and produce an output.
- If the command takes longer, Agent2 can put itself to sleep with its PID.
- The output/error is piped back to the LLM after a `TOOL:` message.
- Conversations are saved as plain text (no json) in `conversation.txt`.
- The text in `conversation.txt` is exactly as the model sees it.
  The conversation includes all the start and stop markers.
- If the model doesn't request another script, the user is prompted.
- The user can stop Agent2 by pressing Ctrl+C

## Example conversation:

Here is an example of a minimal SYSTEM-USER-AGENT-TOOL conversation:

`SYSTEM:` You are Agent2, an Agent that can execute bash scripts
by writting `agent2_script: `

`USER:` list current files!

`LLM:` agent2_script: ls

`TOOL:` boot etc lib run...

`LLM:` These are the entries in the current directory: boot etc lib run...

## Project directory structure:

Here is the directory structure of Agent2:

```text
agent2/
├─ install.sh         # Instalation script
├─ agent2.py          # Contains config + whole python code (single file)
├─ readme.md          # Readme (the file you are currently reading)
├─ context.txt        # Context of the model
├─ prompt.txt         # The initial prompt
├─ conversation.txt   # File where the whole conversation is saved
├─ script.sh          # Script the agent can write and exectute
├─ output.txt         # Output and error of the script.sh
├─ pid.txt            # Process ID, the agent can be paused or killed by other agents 
├─ working_dir/       # The directory where the script is executed.
```

## How to add tools:

Agent2 relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agent's `context.txt` so it knows how to utilize these tools.

Here is an example how to give Agent2 web search capabilities.

First install the software as usual:

```Bash
apt install -y ddgr # Get raw website content
apt install -y curl # Retrieve web search results (`ddgr -x`)
apt install -y lynx # Extract useful text (`curl -s https://www.x.com | lynx -stdin -dump`)
```

Add a note to `context.txt` so the model knows it can use these tools like this:
```text
You can search the web with ddgr, curl, lynx
```

## Multi agent support:

- To make new agents make a copy of Agent2 directory
- Guidance can be given in the model context
- We keep this simple: one program, one agent, one conversation
- Integrating multiagent directly in the program makes everthing much more complex

### Create a new agent:

```bash
# Copy current agent
cp path_agent_dir path_new_agent_dir

# move in to the new agent dir
cd path_new_agent_dir

# Optionally remove existing conversation
> conversation.txt

# Add a prompt to the model by writing to the prompt file
echo "You are a subagent, make a cleanup of..." > prompt

# Launch Agent2:
python3 agent2.py
```
Agent2 doesnt integrate a fixed agent structure.
Agent2 can do this by itself just prompt it right.
Deciding which agent to spawn is up to the agent itself.

## What Agent2 is not:
- No built-in tools:
    With Bash the agent can use all installed CLI tools,
    if an additional tool is required, it needs to be installed and
    added to the LLMs context to make the LLM aware of the tool.
    This keeps Agent2 minimalistic and modular.

- CLI interface only: No GUI overhead
- No guardrails: 
    This is done by user restriction and environments (docker, podman...).
    Linux offers lots of tools to restrict a user.
- No MCP integration: a CLI tool exists for this "`mcp-cli`"
- No Multi-modal: a simple script can handle this: `python-llm`,`aichat`,`curl`
- No memory / No RAG: not an essential feature

## Known issues:
- Infinite Loops: Agent2 can occasionally get stuck in a repetitive loop. 
While there is a built-in counter-mechanism to prevent this, 
you should monitor the agent or set token/spending limits to avoid excessive costs.
- Mid-Response Triggers: Due to model limitations, 
the agent may occasionally include the `agent2_script: ` string while "thinking" or explaining a process. 
This will prematurely trigger command execution.
- Context Retention: The agent may sometimes ignore or forget specific instructions explicitly stated in the initial context (a limitation of the underlying LLM's capabilities).

## Q&A and unsorted notes:

### Why not using a pseudo terminal?
Handling all the controll sequences gets to complicatet.
Just writing to a files and executing is much simpler.
With this the agent can do already a lot. It doesnt need a pseudo terminal.

### Chat tempalates:
Just writing `user:` or `system:` wont work.
Every model needs a specific chat format.
Without this format the model behaves terrible!
The correctness of stop tokens and role markers is crucial for stable behavior.
If you change a model you also need to change these Marker under agent2.py.
You can look them up on the web for each opensource model.

### Will it work for other distros?
Yes, just change the installer `install.sh` to you distros one.
Everthing else stays the same.

### What if i want to turn the agent into sleep?
Agent2 also gives the LLM its own PID and can therefore but itself into sleep with
```text
kill -STOP <PID> && sleep 10 && kill -CONT <PID>
```
This is usefull for reminders, counters and events.

### Why wait exactly 0.2 seconds for the script output?
This was a deliberate design choice because it is simple and effective. Integrating command execution flags is complicated and often fails to cover every scenario due to numerous edge cases. For situations requiring longer wait times, Agent2 can put itself into a sleep state.

### Is Agent2 similar to Claude Code or Agent Zero?
Yes, exactly, but more lightweight.

### Would it be great to also give the LLM the PID of the script?
The script can do this by iteself by adding `echo "Shell PID: $$"`.
For most commands this is not needed becasue they will finish and the shell close automaticly.