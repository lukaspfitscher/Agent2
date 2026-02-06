api_key = "" #add your API-key here!
provider = "https://openrouter.ai/api/v1/completions"
model    = "moonshotai/kimi-k2.5"

#if set to 1, it will read prompt.txt for the first prompt
read_prompt_file = 0


#>> model conversation markers
#im stands for "Instance Message" or simply "Identity Marker."
im_system = "<|im_system|>system<|im_middle|>"
im_user   = "<|im_user|>user<|im_middle|>"
im_llm    = "<|im_assistant|>assistant<|im_middle|>"
im_tool   = "<|im_tool|>tool<|im_middle|>Here is the command output: "
im_end    = "<|im_end|>"
#<<
#>> agent2 markers
im_script = 'agent2_script: '
im_pid    = 'agent2_pid'
#<<
#>> inits
#>> libs
import os, sys, time, subprocess, json, requests
#<<
#>> vars
#vars before functions cause they could be used in the functions
d_a2 = os.path.dirname(os.path.abspath(__file__)) #path of agent2 dir
f_context       = d_a2 +'/context.txt'
f_prompt        = d_a2 +'/prompt.txt'
f_conversation  = d_a2 +'/conversation.txt'
f_script        = d_a2 +'/script.sh'
f_output        = d_a2 +'/output.txt'
#<<
#>> defs

def prnt(txt): print(txt, end="", flush=True)

def user_note(text): prnt(f"\033[93m{text}\033[0m")

def read_file(name):
  with open(name, "r", encoding="latin-1") as f:
    return f.read()

def read_conv(): return read_file(f_conversation)

def write_file(name,txt):
  with open(name, 'w') as f: 
    f.write(txt); f.flush()

def conv_add_file(txt):
  with open(f_conversation, "a") as f:
    f.write(txt); f.flush()

def conv_add(txt): conv_add_file(txt); prnt(txt)

#<<
#<<
#>> check if api key given
if api_key == "": print("\033[91mEnter your API-Key in agent2.py\033[0m"); exit()
#<<
#>> clear conversation
write_file(f_conversation,"")
#<<
#>> append context to conversation
pid = str(os.getpid())

user_note("SYSTEM:↵\n")
conv_add(im_system + read_file(f_context).replace(im_pid, pid) + im_end)

#<<
while True:
  #>> user/file input
  user_note("↵\nUSER:↵\n")
  conv_add(im_user)
  if read_prompt_file == 1:
    user_note("↵\nPROMPT_FILE:↵\n")
    conv_add(read_file(f_prompt))
    read_prompt_file = 0
  else:
    user_note("↵\nINPUT (ctrl+d to send):↵\n")
    #prompt = input()
    #prompt = "".join(sys.stdin)
    prompt = sys.stdin.read() # This reads everything until EOF (Ctrl+D)
    conv_add_file(prompt) #add only to file, terminal already written
  conv_add(im_end)
  #<<
  while True:
    #>> ask llm
    user_note("↵\nLLM:↵\n")
    conv_add(im_llm)
    for l in requests.post(provider,headers={"Authorization": "Bearer " + api_key},
        json={"model": model, "prompt": read_conv(), "temperature": 1, "stream": True},stream=True,).iter_lines():
      if l.startswith(b"data: ") and l != b"data: [DONE]":
        conv_add((json.loads(l[6:])['choices'][0]).get('text','')) #add llm snipes
    conv_add(im_end)
    #<<
    #>> extract command

    #get last LLM response
    LLM_response = read_conv().rsplit(im_llm, 1)[-1]
    if not im_script in LLM_response: break
    write_file(f_script, LLM_response.rsplit(im_script, 1)[-1][:-len(im_end)])

    #<<
    #>> subprocess
    with open(f_output, "w") as f:
      process = subprocess.Popen(
        # or [f_script] if it's executable + has shebang
        ["bash", f_script],
        stdout=f,
        stderr=subprocess.STDOUT,
        #so it's immediately written to the output
        #otherwise it could happen that the agent reads a empty file
        bufsize=0,  # Unbuffered
        # detach from this Python process/session
        start_new_session=True,
        cwd=d_a2 + "/working_dir" )
    
    time.sleep(0.2) #wait for the system to execute and write to file
    #<<
    #>> command feedbacks
    user_note("↵\nTOOL:↵\n")
    conv_add(im_tool+read_file(f_output)+im_end)
    #because it continuously writes to this file and therefore it never gets cleaned
    write_file(f_output,"")
    #<<