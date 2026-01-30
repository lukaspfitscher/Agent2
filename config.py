#provider="https://openrouter.ai/api/v1/chat/completions"
provider = "https://openrouter.ai/api/v1/completions"


model="moonshotai/kimi-k2.5"
#im stands for "Instance Message" or simply "Identity Marker."
im_end    = "<|im_end|>"
im_user   = "<|im_user|>user<|im_middle|>"
im_llm    = "<|im_assistant|>assistant<|im_middle|>"
im_system = "<|im_system|>system<|im_middle|>"

#model="anthropic/claude-haiku-4.5"
#model="anthropic/claude-3-5-sonnet"
#model="openai/gpt-3.5-turbo"
#model="google/gemini-3-flash-preview"

api_key=""

#user   = "\n\nUser:"
#llm    = "\n\nAssistant:"
#system = "\n\nSystem:"