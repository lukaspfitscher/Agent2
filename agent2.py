# Add your API key here!
api_key = ""
provider    = "https://openrouter.ai/api/v1/completions"
model       = "moonshotai/kimi-k2.5"
max_token   = 10000
temperature = 0
read_prompt_file = 0 # 0: User is asked for input in terminal; 1: read first prompt from prompt.txt

## model conversation markers
# "im" stands for "Identity Marker."
im_system = "<|im_system|>system<|im_middle|>"
im_user   = "<|im_user|>user<|im_middle|>"
im_llm    = "<|im_assistant|>assistant<|im_middle|>"
im_tool   = "<|im_user|>user<|im_middle|>" #"<|im_tool|>tool<|im_middle|>"
im_end    = "<|im_end|>"
## Agent2 markers, used for script start keyword
im_script        = "agent2_script_start"
# This msg is given the llm after every script execution
tool_explanation = "This is an automatically generated message. Script execution started. Here is the output (if any) after 0.2 seconds:"
## Inits
import os, sys, requests, time, subprocess, json
#from prompt_toolkit import prompt
## Vars
# Path of the agent2 dir
d_a2 = os.path.dirname(os.path.abspath(__file__))
f_context       = d_a2 +"/context.txt"
f_prompt        = d_a2 +"/prompt.txt"
f_conversation  = d_a2 +"/conversation.txt"
f_script        = d_a2 +"/script.sh"
f_output        = d_a2 +"/output.txt"
f_pid           = d_a2 +"/pid.txt"
d_working       = d_a2 +"/working_dir"

#printing without newline at the end
def prnt(txt): print(txt, end="", flush=True)

def print_yellow(text): prnt(f"\033[93m{text}\033[0m")

def read_file(name):
  with open(name, "r", encoding="utf-8") as f:
    return f.read()

def read_conv(): return read_file(f_conversation)

def write_file(name,txt):
  with open(name, 'w', encoding="utf-8", errors="replace") as f: 
    f.write(txt); f.flush()

# Add input only to the file, already written to the terminal
def conv_add_file(txt):
  with open(f_conversation, "a") as f: f.write(txt); f.flush()

# Add text to conversation file and also print
def conv_add(txt): conv_add_file(txt); prnt(txt)

## Check if API key is given
if api_key == "": 
  print("\033[91mNo API key! Enter your API key in agent2.py. Program terminated!\033[0m")
  exit()
## Clear conversation
write_file(f_conversation,"")
# Add program PID to file
write_file(f_pid,str(os.getpid()))

print_yellow("SYSTEM:↵\n")
conv_add(im_system + read_file(f_context) + im_end)

while True:
  ## User/file input
  print_yellow("↵\nUSER:↵\n")
  conv_add(im_user)
  if read_prompt_file == 1:
    print_yellow("↵\nPROMPT_FILE:↵\n")
    conv_add(read_file(f_prompt))
    read_prompt_file = 0
  else:
    print_yellow("↵\nINPUT:↵\n")
    user_input = input()
    conv_add_file(user_input)
  conv_add(im_end)
  while True:
    ## send to LLM
    print_yellow("↵\nLLM:↵\n")
    conv_add(im_llm)
    for l in requests.post(provider,headers={"Authorization": "Bearer " + api_key},
        json={"model": model, "prompt": read_conv(), "temperature": temperature,"stop": [im_end], "stream": True}, stream=True,).iter_lines():
      if l.startswith(b"data: ") and l != b"data: [DONE]":
        conv_add((json.loads(l[6:])['choices'][0]).get('text','')) # Add LLM snippets
        if len(read_conv()) // 4 > max_token: #check if max_token is reached
          print("\033[91mToken limit reached. You can adjust max_token in the agent.py file. Program terminated!\033[0m"); exit()
    conv_add(im_end)

    ## Extract command
    # Get last LLM response
    LLM_response = read_conv().rsplit(im_llm, 1)[-1]
    if not im_script in LLM_response: break
    # -1: start from the end
    write_file(f_script, LLM_response.rsplit(im_script, 1)[-1][:-len(im_end)])
    # Subprocess
    with open(f_output, "w") as f:
      process = subprocess.Popen(
        ["bash", f_script],
        stdout=f,
        stderr=subprocess.STDOUT,
        # So it's immediately written to the output
        # Otherwise it could happen that the agent reads an empty file
        bufsize=0, # Unbuffered
        # Detach from this Python process/session
        start_new_session = True,
        cwd=d_working )

    # Wait for the system to execute and write to file
    time.sleep(0.2)
    ## Command feedbacks
    print_yellow("↵\nTOOL:↵\n")
    conv_add(im_tool+tool_explanation+read_file(f_output)+im_end)
    #conv_add(+read_file(f_output))
    # It keeps writing to this file, so it never gets cleared automatically
    write_file(f_output,"")