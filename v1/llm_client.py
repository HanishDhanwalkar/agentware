# from typing import Dict, List, Any, Callable, Optional, Union
# import json
# import 


# class LLMClient:
#     """Simple wrapper for LLM API calls"""
    
#     def __init__(self, model="gpt-3.5-turbo"):
#         self.model = model
        
#     def model_init(self, model: str):
#         openai_models = ["gpt-3.5-turbo", "gpt-4"]
#         if self.model in openai_models:
#             try:
#                 from openai import OpenAI
#                 client = OpenAI()
#                 client.chat.completions.create(model=model)
#                 self.model = model
#             except Exception as e:
#                 print(f"Error initializing OpenAI model: {str(e)}")
                
#     def generate_response(self, 
#                          messages: List[Dict[str, str]], 
#                          tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
#         """Generate a response from the LLM"""
#         try:
#             from openai import OpenAI
#             client = OpenAI()
            
#             # Prepare the API call
#             kwargs = {
#                 "model": self.model,
#                 "messages": messages,
#             }
            
#             # Add tools if provided
#             if tools:
#                 kwargs["tools"] = tools
#                 kwargs["tool_choice"] = "auto"
            
#             # Make the API call
#             response = client.chat.completions.create(**kwargs)
            
#             # Convert API response to dictionary for easier handling
#             response_message = response.choices[0].message
#             result = {
#                 "content": response_message.content,
#                 "tool_calls": None
#             }
            
#             # Extract tool calls if present
#             if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
#                 result["tool_calls"] = []
#                 for tool_call in response_message.tool_calls:
#                     result["tool_calls"].append({
#                         "id": tool_call.id,
#                         "name": tool_call.function.name,
#                         "arguments": json.loads(tool_call.function.arguments)
#                     })
            
#             return result
        
#         except ImportError:
#             print("Error: OpenAI package not installed. Run 'pip install openai'")
#             return {"content": "Error: OpenAI package not installed", "tool_calls": None}
#         except Exception as e:
#             print(f"Error calling LLM API: {e}")
#             return {"content": f"Error: {str(e)}", "tool_calls": None}
