# Agent2

A lightweight AI agent that can control your computer by executing Bash scripts

## Introduction:

- Agent2 controls a machine by writing a bash script at the end of its response.
The script will be extracted from the response of the LLM, 
executed and the output/error will be piped back to the LLM.
Thats it nothing more!

- Agent2 tries to be minimalistic and focuses on essentials. With only ~130 lines of Python code, 
Agent2 is short, simple / very light / easy to understand / easy to extend and still quite capable.

- Agent2 relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with relevant tools
and update `context.txt` so the LLM knows how to utilize these tools.
Under the "How to add tools" section, there is an example.

> A human can do a lot with a script/terminal, therefore, an agent can do it as well.
> The more agents/LLM's advance the less framework is required.
> Because it's so simple, Agent2 is an Agent framework for Agents

Agent2 is programmed in Python, Open-source on [Github](https://github.com/lukaspfitscher/Agent2)
and written by Lukas Pfitscher (feedback is appreciated: lukaspfitscher1996@gmail.com)"

## Quick setup:

- Be in the directory where agent2 should be copied, then download with:
```bash
curl -L -o agent2.zip https://github.com/lukaspfitscher/Agent2/archive/refs/heads/main.zip
```
- Extract the directory, remove the .zip file and rename it:
```bash
unzip agent2.zip; rm agent2.zip; mv Agent2-main agent2
```
- Only `python3` and the `requests` library are required to run Agent2. To install do:
```bash
cd agent2; chmod +x install.sh; ./install.sh
```
or just paste the following command into your terminal:
```bash
apt update; apt install -y python3 python3-pip python3-requests
```
- Next add your Openrouter API key in the `agent2.py` file.

- Optionally, also adjust the token limit in the `agent2.py` file.

- Launch Agent2 with (Be careful! It can control your system!):
```bash
python3 agent2.py
```

## System prompt / context:

Here is the discription how Agent2 behaves:

You are Agent2, the best tinkerer, engineer, scientific researcher and coding agent.
- You possess common sense, are logic-driven, and are helpful.
- You remain concise and precise with your answers.
- No feelings. No guessing. Rely on hard scientific truths and facts.
- You are maximally truth-seeking, even if the subject is controversial.
- You think in a clean, structured way. You plan / make todo lists / think step by step for the requested task if needed.

## Environment:

- Agent2 can run directly on your local machine, server, 
VPS or in an environment (docker, podman...).

## Protocol overview:

- The file `context.txt` contains the context of the model, like "You are Agent2, a..."
- Everything written to the terminal or in the `conversation.txt`.
  file is exactly as it is seen by the LLM,
  except the yellow notes in the terminal for better user visualization.
- The user can input after an `INPUT:`.
- For user input, the Enter key is a normal new line,
  submit with Ctrl+D (standard Unix convention for 'end of input').
- The LLM responds with `LLM:`.
- The communication between LLM and host is kept simple:
  The LLM triggers script execution by writing: `agent2_script_start`
- After the last `agent2_script_start` all the text is copied into `script.sh`
- Before every execution the script is reset (path doesnt persist, no environment variables persist).
- After that, the script gets executed in a separate shell and therefore doesn't block the agent.
- The script always starts in the `working_dir` directory.
- The script output is written to the `output.txt` file.
- Agent2 waits 0.2 seconds for the command to finish and read from `output.txt`.
- If the command takes longer, Agent2 can put itself to sleep with its own PID.
- The output/error is piped back to the LLM after a `TOOL:` message.
- Conversations are saved as plain text (no json) in `conversation.txt`.
- The text in `conversation.txt` is exactly as the model sees it.
  The conversation includes all the start and stop markers.
- If the model doesn't request another script, the user is prompted for input.
- The user can stop Agent2 by pressing Ctrl+C.

## Example conversation:

Here is an example of a minimal SYSTEM-USER-LLM-TOOL conversation:

`SYSTEM:` You are Agent2, an Agent that can execute bash scripts
by writing `agent2_script_start` at the end of your response...

`USER:` list current files!

`LLM:` agent2_script_start ls -a

`TOOL:` . .. boot etc lib run...

`LLM:` Entries in the current directory: boot etc lib run...

## Project directory structure:

Here is the directory structure of Agent2:

```text
agent2/
├─ install.sh       # Installation script
├─ agent2.py        # Contains config + whole python code (single file)
├─ readme.md        # Readme / documentation (the file you are currently reading)
├─ context.txt      # Context of the model ( like role description )
├─ prompt.txt       # The initial prompt
├─ conversation.txt # File where the whole conversation is saved
├─ script.sh        # Script the agent can write to and execute
├─ output.txt       # Output and error of the script.sh
├─ pid.txt          # Process ID, the agent can be paused or killed by other agents
├─ working_dir/     # Working directory of the agent; starting path of the script
```

## How to add tools:

Agent2 relies on the host's CLI environment.
To ensure Agent2 is productive, provide it with the relevant tools
and update the agent's `context.txt` so it knows how to utilize these tools.

Here is an example of how to give Agent2 web search capabilities.

First install the software as usual:

```Bash
apt install -y ddgr # Get web search results (DuckDuckGo search;`ddgr -x search_keyword`)
apt install -y curl # Get raw website content
apt install -y lynx # Extract useful text (`curl -s https://www.x.com | lynx -stdin -dump`)
```

Add a note to `context.txt` so the model knows it can use these tools:
```text
You can search the web with ddgr, curl, lynx
```

## Multi-agent support:

- New agents can be made by simply coping Agent2's directory.
- Guidance can be given in the model context.
- This is keept simple: one program, one agent, one conversation. 
Integrating multi-agent directly in the program makes everything much more complex.

### Create a new agent:

```bash
# Copy current agent
cp "path_agent_dir" "path_new_agent_dir"

# Move in to the new agent dir
cd "path_new_agent_dir"

# Clear existing conversation
> conversation.txt

# Clear the agents working directory
rm -rf working_dir/*

# Add a prompt to the model by writing to the prompt file
echo "You are a subagent, make a cleanup of..." > prompt.txt

# Launch Agent2:
python3 agent2.py
```
Agent2 doesn't integrate a fixed agent structure.
Deciding which agent to spawn is up to the agent itself.
Agent2 can do this by itself just prompt it right.

## Known issues:

- Agent2 can occasionally get stuck in a repetitive loop. 
There is a built-in counter-mechanism to prevent this. 
Set `max_tokens` in `agent2.py` to limit token/spending.
- Mid-Response Triggers: Due to model limitations, 
the agent may occasionally include the `agent2_script_start` string while "thinking" or explaining a process.
This will prematurely trigger command execution.
- The agent may sometimes ignore or forget specific instructions 
explicitly stated in the initial context (a limitation of the underlying LLM's capabilities).
- If the LLM is not explicitly told 'script executed', 
it will think it didn't work and repeat itself over and over.

## What Agent2 is not:
- No built-in tools:
    With Bash the agent can use all installed CLI tools,
    if an additional tool is required, it needs to be installed and
    added to the LLM's context to make the LLM aware of the tool.
    This keeps Agent2 minimalistic and modular.

- CLI interface only: No GUI overhead
- No guardrails: 
    This is done by user restriction and environments (docker, podman...).
    Linux offers lots of tools to restrict a user.
- No MCP integration: a CLI tool exists for this "`mcp-cli`"
- No Multi-modal: a simple script can handle this: `python-llm`,`aichat`,`curl`
- No memory / No RAG: not an essential feature

## Q&A and unsorted notes:

### Why not using a pseudo terminal?
Handling all the control sequences gets too complicated.
Writing to a file and executing it is much simpler.
With this, the agent can already do a lot. It doesn't need a "pseudo-terminal".

### Chat templates:
Just writing `user:` or `system:` won't work.
Every model needs a specific chat format.
The model is trained on these markers.
Without this format the model behaves terribly!
The correctness of stop tokens and role markers is crucial for stable behavior.
If you change a model you also need to change these markers in agent2.py.
You can look them up on the web for each open-source model.

### Will it work for other distros?
Yes, just change `install.sh` to your distro’s installer.
Everything else stays the same.

### What if the agent needs to wait for a certain time, like for a download to finish?
The PID of the python program running agent2 (not the seperate shell the agent can execute) 
is saved in the `pid.txt` file.
With it Agent2 can put itself to sleep with:
```bash
PID="$(< ../pid.txt)" #read pid from file
kill -STOP "$PID" && sleep 10 && kill -CONT "$PID" 
```
This is useful for waiting for commands (like waiting for downloads, monitoring), reminders and counters.
The PID is saved in the `pid.txt` file so other programs/agents have control over the current agent.

### Why wait exactly 0.2 seconds for the script output?
This was a deliberate design choice because it is simple and effective.
0.2s handles the fast commands (ls, cat, echo, etc.) — which are most commands.
Integrating command execution flags is complicated and often fails to cover every scenario 
due to numerous edge cases (some commands continue writing and therefore never finish, 
or a script can contain multiple programs).
For situations requiring longer wait times, Agent2 can put itself into a sleep state.

### Is Agent2 similar to Claude Code or Agent Zero?
Yes, exactly, but more lightweight.

### Would it be useful to also give the LLM the PID of the script?
The script can do this by itself by adding `echo "Shell PID: $$"`.
For most commands this is not needed because they will finish and the shell closes automatically.

### Why not use common chat completion and JSON chat templates?
We believe this overcomplicates things. 
An LLM is fundamentally text in, text out — 
and we should treat it as such. Because we use completion mode, 
only open-source models are available. 
Closed-source models don't publish their chat templates, 
so they aren't compatible with this project. 
However, you can easily change to normal json chat conversation— 
just ask an LLM to modify the agent2.py file.

### Why is the context.txt so long?
Turns out you can give the LLM long instructions 
and it will actually perform better. 
These LLM context texts are carefully tested to work properly.
