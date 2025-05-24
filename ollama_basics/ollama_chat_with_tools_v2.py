# ref: https://ollama.com/blog/functions-as-tools

import ollama
import requests

def add_two_numbers(a: float, b: float) -> int:
    """
    Add two numbers

    Args:
      a: The first integer number
      b: The second integer number

    Returns:
      int: The sum of the two numbers
    """
    a= float(a)
    b= float(b)
    return a + b


response = ollama.chat(
    'llama3.2',
    messages=[{'role': 'user', 'content': 'What is 10 + 10?'}],
    tools=[add_two_numbers, requests.request], # Actual function reference
)

available_functions = {
    'add_two_numbers': add_two_numbers,   
}

for tool in response.message.tool_calls or []:
    function_to_call = available_functions.get(tool.function.name)
    # print(function_to_call)
    # print(**tool.function.arguments)
    print(response)
    print(type(response))
    
    if function_to_call is not None:
      print('Function found:', tool.function.name)
      print('Function arguments:', tool.function.arguments)
      print(function_to_call(**tool.function.arguments))
      
    # if function_to_call:
    #     print('Function output:', function_to_call(**tool.function.arguments))
    # else:
    #     print('Function not found:', tool.function.name)