from ollama import Client
import json
# import argparse

# parser = argparse.ArgumentParser()

# parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging", default=False)
# parser.add_argument("--model", "-m", choices=["llama3.2", "deepseek-r1:7b"], help="LLM model to use", default="llama3.2")
# parser.add_argument("--stream", "-s", action="store_true", help="Enable stream mode", default=False)

# args = parser.parse_args()

# print(args)


MODEL = "llama3.2"
# MODEL = "deepseek-r1:7b" 

STREAM = True


# TOOLS Definations STARTS HERE
TOOLS = []
def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
        a: The first integer number
        b: The second integer number

    Returns:
        int: The sum of the two numbers
    """
    return a + b

TOOLS.append(add_two_numbers)
# TOOLS Definations ENDS HERE

def input_to_llm(prompt):
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ],
        "tools": TOOLS,
    }
    
    # print(data)
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
        response = ""
        stream_response = client.chat(
            **data,
            stream=True,
            
        )
        for s in stream_response:
            chunk = s.get("message", {}).get("content", "")
            response += chunk
            print(chunk, end="")
    
    else:
        response = client.chat(
            **data
            )
        print(response.get("message", {}).get("content", ""))
    
    available_functions = {
        'add_two_numbers': add_two_numbers,
    }
    
    print(response)
    print(type(response))

    for tool in response.get('tool_calls'):
        function_to_call = available_functions.get(tool.function.name)
    if function_to_call:
        print('Function output:', function_to_call(**tool.function.arguments))
    else:
        print('Function not found:', tool.function.name)
        
if __name__ == "__main__":
    main()
    