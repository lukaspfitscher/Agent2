<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent2 - Minimal Terminal Agent</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #a0e0d0;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .bg-lights {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }

        .light-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.4;
            animation: float 20s infinite ease-in-out;
        }

        .light-orb:nth-child(1) {
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, #00ffaa 0%, transparent 70%);
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }

        .light-orb:nth-child(2) {
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, #00aaff 0%, transparent 70%);
            top: 60%;
            right: 10%;
            animation-delay: -5s;
        }

        .light-orb:nth-child(3) {
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, #00ffcc 0%, transparent 70%);
            bottom: 20%;
            left: 30%;
            animation-delay: -10s;
        }

        .light-orb:nth-child(4) {
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, #44ddff 0%, transparent 70%);
            top: 30%;
            right: 30%;
            animation-delay: -15s;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(100px, -50px) scale(1.1); }
            50% { transform: translate(-50px, 100px) scale(0.9); }
            75% { transform: translate(-100px, -100px) scale(1.05); }
        }

        .content {
            position: relative;
            z-index: 10;
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 20px;
        }

        header {
            text-align: center;
            margin-bottom: 60px;
        }

        h1 {
            font-size: 4rem;
            color: #00ffaa;
            text-shadow: 0 0 20px #00ffaa55, 0 0 40px #00ffaa33;
            margin-bottom: 10px;
            letter-spacing: 4px;
        }

        .tagline {
            font-size: 1.2rem;
            color: #66ddcc;
            opacity: 0.8;
        }

        .section {
            background: rgba(0, 40, 40, 0.3);
            border: 1px solid #00ffaa33;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            transition: box-shadow 0.3s ease;
        }

        .section:hover {
            box-shadow: 0 0 30px #00ffaa22, inset 0 0 20px #00ffaa11;
            border-color: #00ffaa66;
        }

        h2 {
            color: #00ddff;
            font-size: 1.5rem;
            margin-bottom: 15px;
            text-shadow: 0 0 10px #00ddff44;
        }

        h3 {
            color: #00ccff;
            font-size: 1.2rem;
            margin-bottom: 12px;
            margin-top: 20px;
        }

        p {
            line-height: 1.8;
            margin-bottom: 15px;
            color: #99ddcc;
        }

        .quote {
            font-style: italic;
            color: #00ffaa;
            border-left: 3px solid #00ffaa;
            padding-left: 20px;
            margin: 20px 0;
        }

        code {
            background: rgba(0, 255, 170, 0.1);
            padding: 3px 8px;
            border-radius: 4px;
            color: #00ffcc;
            font-size: 0.9rem;
        }

        .terminal {
            background: #0d1a1a;
            border-radius: 8px;
            overflow: hidden;
            margin: 20px 0;
        }

        .terminal-body {
            padding: 20px;
            font-size: 0.9rem;
        }

        .terminal-line {
            margin-bottom: 8px;
        }

        .prompt-user { color: #ffaa00; }
        .prompt-agent { color: #00aaff; }
        .prompt-system { color: #00ff88; }

        ul {
            margin-left: 20px;
            margin-bottom: 15px;
            color: #99ddcc;
        }

        li {
            margin-bottom: 8px;
            line-height: 1.6;
        }

        .warning {
            background: rgba(255, 170, 0, 0.1);
            border-left: 3px solid #ffaa00;
            padding: 15px;
            margin: 20px 0;
            color: #ffcc66;
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            color: #446655;
            font-size: 0.9rem;
        }

        .glow-text {
            animation: glow 3s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 20px #00ffaa55, 0 0 40px #00ffaa33; }
            to { text-shadow: 0 0 30px #00ffaa88, 0 0 60px #00ffaa55; }
        }
    </style>
</head>
<body>
    <div class="bg-lights">
        <div class="light-orb"></div>
        <div class="light-orb"></div>
        <div class="light-orb"></div>
        <div class="light-orb"></div>
    </div>

    <div class="content">
        <header>
            <h1 class="glow-text">Agent2</h1>
            <p class="tagline">Minimal Terminal Agent for LLMs</p>
        </header>

        <div class="section">
            <h2>Short Description</h2>
            <p>Agent2 is a minimal Agent that can execute bash commands</p>
            <div class="warning">
                This project doesn't exist yet!! just my thoughts of a great Agent :)
            </div>
        </div>

        <div class="section">
            <h2>Introduction</h2>
            <p>Agent2 is a program that lets a LLM (Large Language Model) control a Linux machine by executing bash commands.</p>
            <p>It can controls a machine by writing bash commands at the end of its prompt. The program will than execute the commands and pipe back the output/error to the LLM. Agent2 tries to be minimalistic and only focus on essentials working things.</p>
            <p>Agent2 has no built-in tools. It relies on the host's CLI environment. Therefore to ensure Agent2 is productive, provide it with the relevant CLI tools and update its preprompt so it knows how to utilize them. A great toolkit is ATK, it's a standardised toolkit for agentic task for general purpose workflows.</p>
            <p>It is compatible with major LLM providers like Openrouter (all models), Anthropic (claude), xAI (Grok), Google (Gemini)... Agent2 is similar to Claude Code, or Agent Zero but more minimalistic</p>
            <div class="quote">"A human can do a lot with a terminal, therefore, a terminal agent can do it as well"</div>
            <p>Agent2 is programmed in <code>C</code> and Open-source</p>
        </div>

        <div class="section">
            <h2>Setup / Examples</h2>
            <p>Here are some common commands to setup Agent2:</p>
            <p>There is already a prebuild example agent called "example_agent" to get starting easy</p>
            
            <div class="terminal">
                <div class="terminal-body">
                    <div class="terminal-line"><span class="prompt-system"># Creates a new agent</span></div>
                    <div class="terminal-line"><span class="prompt-system"># You can setup different agents by giving them a different name</span></div>
                    <div class="terminal-line">agent2 -name "my_agent"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># All Agent2 settings after a target command will target the target (persist)</span></div>
                    <div class="terminal-line">agent2 -target "my_agent"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Enter your API-key:</span></div>
                    <div class="terminal-line">agent2 -api_key "API-KEY"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Set a provider:</span></div>
                    <div class="terminal-line"><span class="prompt-system"># eg "https://openrouter.ai/api/v1/chat/completions" for openrouter</span></div>
                    <div class="terminal-line">agent2 -provider "your_provider"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Set model</span></div>
                    <div class="terminal-line">agent2 -model "anthropic/claude-3.5-sonnet"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Set model temperature:</span></div>
                    <div class="terminal-line">agent2 -temperature 0.8</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Start Agent2 with a prompt (Ctrl + c to stop):</span></div>
                    <div class="terminal-line">agent2 -prompt "what is the meaning of life?"</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># limit the agents token/ cost (if it ever goes rogue):</span></div>
                    <div class="terminal-line"><span class="prompt-system"># write "nolimit" for unlimited tokens</span></div>
                    <div class="terminal-line">agent2 -max_tokens 20000</div>
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system"># Launch an Agent2 agent with minimal settings:</span></div>
                    <div class="terminal-line">agent2 -name "my_agent" -max_tokens 2000 -model "anthropic/claude-3.5-sonnet" -prompt "return the sum of 34+45"</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>What Agent2 is not</h2>
            <ul>
                <li><strong>No GUI overhead</strong></li>
                <li><strong>No memory feature / No RAG:</strong> not an essential feature</li>
                <li><strong>No MCP integration:</strong> a CLI tool exists for this "mcp-cli"</li>
                <li><strong>No guardrails:</strong> linux offers lots of tools to restrict a user</li>
                <li><strong>No built-in tools:</strong> Bash is enough, if a tool is necessary, it is a separate program that needs to be installed and added to the preprompt to make the model aware. This keeps Agent2 modular and minimalistic.</li>
                <li><strong>No fixed agent structure:</strong> Deciding which agent to spawn is up to the agent itself. Guidance can be given in the preprompt</li>
                <li><strong>No Multi-modal:</strong> CLI tools can handel this like python-llm, aichat, curl</li>
            </ul>
        </div>

        <div class="section">
            <h2>Environment</h2>
            <p>Because it's a CLI tools the agent doesn't care if it runs directly on your local machine or in a environment (docker, podman...)</p>
        </div>

        <div class="section">
            <h2>Protocol</h2>
            <p>The communication protocol is kept simple: To execute a command the LLM wraps the command in special word <code>agent2_command_start</code> and <code>agent2_command_end</code> at the end of its response. The program will than execute the command and pipe back the output/error to the LLM</p>
        </div>

        <div class="section">
            <h2>CLI Interface</h2>
            <ul>
                <li>The agent responds with a blue "AGENT:" + newline</li>
                <li>The user can input after a orange "USER:" + newline</li>
                <li>If the model doesn't requests a command the user is prompted</li>
                <li>The user can finish its input with Ctrl+D - Standard Unix "end of input"</li>
                <li>Enter will print a normal new line</li>
            </ul>
        </div>

        <div class="section">
            <h2>Example Conversation</h2>
            <p>Here is an example of a USER-AGENT-SYSTEM conversation:</p>
            
            <div class="terminal">
                <div class="terminal-body">
                    <div class="terminal-line"><span class="prompt-user">USER:</span></div>
                    <div class="terminal-line">You are Agent2, a Agent that can execute programs</div>
                    <div class="terminal-line">by wrapping a bash command with agent2_command_start and agent2_command_end</div>
                    <div class="terminal-line">at the end of your prompt.</div>
                    <div class="terminal-line">You can ask for user input with the cat bash function.</div>
                    <div class="terminal-line">Here is a list of useful programs: ls, cd, curl...</div>
                    <div class="terminal-line">list current files!</div>
                    
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-agent">AGENT:</span></div>
                    <div class="terminal-line">agent2_command_start</div>
                    <div class="terminal-line">ls</div>
                    <div class="terminal-line">agent2_command_end</div>
                    
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-system">SYSTEM:</span></div>
                    <div class="terminal-line">boot etc lib run...</div>
                    
                    <div class="terminal-line" style="margin-top: 15px;"><span class="prompt-agent">AGENT:</span></div>
                    <div class="terminal-line">This are the entries in the current directory:</div>
                    <div class="terminal-line">boot etc lib run...</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Project Directory Structure</h2>
            <p>Here is the directory structure of Agent2:</p>
            
            <div class="terminal">
                <div class="terminal-body">
                    <div class="terminal-line">agent2</div>
                    <div class="terminal-line">  agent2   <span class="prompt-system"># bash script to execute /bin/agent2</span></div>
                    <div class="terminal-line">  conv     <span class="prompt-system"># conversation history</span></div>
                    <div class="terminal-line">    251101_104950_961975220</div>
                    <div class="terminal-line">    251101_104840_703965980</div>
                    <div class="terminal-line">    251101_104837_697176974</div>
                    <div class="terminal-line">  config</div>
                    <div class="terminal-line">    program</div>
                    <div class="terminal-line">    agents</div>
                    <div class="terminal-line">      agent_name1  <span class="prompt-system"># agent configurations</span></div>
                    <div class="terminal-line">      agent_name2</div>
                    <div class="terminal-line">      ...</div>
                    <div class="terminal-line">  dev</div>
                    <div class="terminal-line">    agent2    <span class="prompt-system"># executable</span></div>
                    <div class="terminal-line">    agent2.c  <span class="prompt-system"># source code</span></div>
                </div>
            </div>
        </div>

        <footer>
            <p>Agent2 — Open Source Terminal Agent</p>
            <p style="margin-top: 10px;">Similar to Claude Code & Agent Zero, but more minimalistic</p>
        </footer>
    </div>
</body>
</html>
