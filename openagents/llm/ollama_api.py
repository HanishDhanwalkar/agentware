from ollama import Client

client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

# TODO: deepseek api handling


model = "llama3.2"
# model = "deepseek-r1:7b" 

prompt = "Choose a number between 1 and 10. No thinking, just respond with the number."

stream = True 

data = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": f"{prompt}",
        },
    ] 
}

if stream:
    stream_response = client.chat(
        **data,
        stream=True,
    )
    for s in stream_response:
        print(s.get("message", {}).get("content", ""), end="")
  
else:
    response = client.generate(**data)
    print(response.get("message", {}).get("content", ""))
    
    
    
# curl http://localhost:11434/api/generate -d '{
#   "model": "deepseek-r1:7b",
#   "prompt": "Why is the sky blue?",
#   "stream": false
# }'

# curl http://localhost:11434/api/generate -d '{
#   "model": "deepseek-r1:7b",
#   "prompt": "Why is the sky blue?",
#   "stream": false
# }'