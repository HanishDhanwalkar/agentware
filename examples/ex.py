import logging
import sys
import os

# Add the parent directory to sys.path to allow importing the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from openagents import create_agent

agent = create_agent(
    name="MyAgent",
    system_prompt="You are a specialized agent that in English literature",
    llm_model="llama3.2",
    verbose=True,
)

# Process user inputs
response = agent.process_input("Write a poem in English about a cat")

print(response)