import logging
import sys
import os
import argparse

# Add the parent directory to sys.path to allow importing the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

args = argparse.ArgumentParser()
args.add_argument(
    "--verbose", "-v", action="store_true", help="Enable verbose logging", default=True
)
args.add_argument(
    "--model", "-m", choices=["llama3.2", "deepseek-r1:7b"], help="LLM model to use", default="llama3.2"
)

args = args.parse_args()

from openagents import create_agent

agent = create_agent(
    name="MyAgent",
    system_prompt="You are a specialized agent that in English literature",
    llm_model=args.model,
    verbose=args.verbose,
)

# Process user inputs
response = agent.process_input("Write a poem in English about a cat")

print(response)