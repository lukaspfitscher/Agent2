#>> user setting
provider="https://openrouter.ai/api/v1/chat/completions"
model="anthropic/claude-3-5-sonnet"
#model="openai/gpt-3.5-turbo"
#model="google/gemini-3-flash-preview"
api_key="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"


#<<
#>> libs
import os
import sys
import time
import subprocess
import requests,json
#<<
#>> vars
#vars before functions casue they could be used in the functions
file_dir = os.path.dirname(os.path.abspath(__file__))
modules        = file_dir + '/..'
f_conversation = file_dir + '/conversation'
f_script       = file_dir + '/script'
f_output       = file_dir + '/output'
f_context      = file_dir + '/context'
conversation   = ''
#<<
#>> defs
def run(path): subprocess.run(["python3", path])

def sleep(seconds):time.sleep(seconds)

def prnt(string):
  print(string, end="", flush=True)

def write_file(name,txt):
  with open(name, 'w') as file: 
    file.write(txt)
    file.flush()

def append_to_conv(string):
  with open(f_conversation, "a") as f:
    f.write(string)
    f.flush()

def append_to_conv_and_terminal(string):
  append_to_conv(string)
  prnt(string)

#strange string imutable need to use return
def read_file(file_name):
  with open(file_name, "r", encoding="utf-8") as file: return file.read()
#<<
#>> append context to conversation
append_to_conv_and_terminal("\n\nSYSTEM:\n\n")
context = read_file(f_context)
current_pid = os.getpid()
append_to_conv(context)
conversation = read_file(f_conversation)
prnt(conversation)
#<<
while True:
  #>> user input
  append_to_conv_and_terminal("\n\nUSER:\n\n")
  text = sys.stdin.read() # This reads everything until EOF (Ctrl+D)
  append_to_conv(text)
  #<<
  while True:
    #>> ask llm
    conversation = read_file(f_conversation)
    append_to_conv_and_terminal("\n\nLLM:\n\n")

    res = requests.post(provider,
      headers={"Authorization":"Bearer "+api_key},
      json={"model":model,
        "messages":[{"role":"user","content":conversation}],
        "stream":True}, stream=True)

    for l in res.iter_lines():
      if l.startswith(b"data: ") and l!=b"data: [DONE]":
        content = json.loads(l[6:])['choices'][0]['delta'].get('content','')
        append_to_conv_and_terminal(content)

    conversation = read_file(f_conversation)
    #<<
    #>> extract command
    start_token="agent2_script_start\n"
    end_token="\nagent2_script_end"

    #first check if the end tocken exists at the end of the conversation
    if not conversation.endswith(end_token):
      #if no end_token write nothing to script.sh and finish
      command_found = 0
      write_file(f_script,"")

    else:
      command_found = 1
      #extract the text between the last end_token and last start_token
      last_end_idx = conversation.rfind(end_token)
      last_start_idx = conversation.rfind(start_token, 0, last_end_idx)

      #-1 means string not found
      if last_start_idx != -1:
        extracted_text = conversation[last_start_idx + len(start_token):last_end_idx]
        #save the text to f_script
        write_file(f_script,extracted_text)
    #<<
    if command_found == 0: break
    #>> supprocess
    with open(f_output, "w") as f:
      process = subprocess.Popen(
        # or [f_script] if it's executable + has shebang
        ["bash", f_script],
        stdout=f,
        stderr=subprocess.STDOUT,
        #so its imidatly wrote to the output
        #otherwise it could happen that the agent reads a emty file
        bufsize=0,  # Unbuffered
        # detach from this Python process/session
        start_new_session=True )
    
    # Save the PID to a file
    pid_path = file_dir+'/pid'
    with open(pid_path, "w") as pid_file:
        pid_file.write(str(process.pid))

    #wait a bit so the system has time to execute and write to file
    import time
    time.sleep(0.5)
    #<<
    #>> append output to conversation
    output = read_file(f_output)
    append_to_conv_and_terminal("\n\nSYSTEM:\n\n" + output )
    #<<