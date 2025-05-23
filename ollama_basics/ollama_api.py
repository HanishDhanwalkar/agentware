from ollama import Client

MODEL = "llama3.2"
# MODEL = "deepseek-r1:7b" 

STREAM = True

def input_to_llm(prompt):
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ] 
    }
    return data

def main():
    client = Client(
        host='http://localhost:11434',
        headers={'x-some-header': 'some-value'}
    )

    prompt = input("Enter a prompt: (press enter for deafault prompt) ")
    if prompt == "":
        prompt = "Choose a number between 1 and 10. No thinking, just respond with the number."

    data = input_to_llm(prompt)

    if STREAM:
        stream_response = client.chat(
            **data,
            stream=True,
        )
        for s in stream_response:
            print(s.get("message", {}).get("content", ""), end="")
    
    else:
        response = client.chat(**data)
        print(response.get("message", {}).get("content", ""))
        
if __name__ == "__main__":
    main()
        
        
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