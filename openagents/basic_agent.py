"""
Basic example of using the OpenAgents framework.
"""
import logging
import sys
import os

# Add the parent directory to sys.path to allow importing the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openagents.core.agent import Agent
from openagents.llm.ollama import OllamaLLM
from openagents.tools.registry import ToolRegistry
from openagents.tools.general import GeneralTools


def main():
    """Run a basic example of the OpenAgents framework"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create LLM client
    # You can change the model to any model available in your Ollama installation
    llm = OllamaLLM(model="llama3.2")  # or "mistral", "phi", etc.
    
    # Create tool registry and register tools
    registry = ToolRegistry()
    registry.register_provider(GeneralTools())
    
    # Create agent
    agent = Agent(
        name="OpenAgent",
        system_prompt="You are a helpful AI assistant with access to tools. Use them when appropriate to provide accurate information.",
        llm=llm,
        tool_registry=registry,
        verbose=True
    )
    
    print(f"\n{agent.name}: Hello! I'm your AI assistant. I can help you with various tasks using tools.")
    print("Type 'exit' to end the conversation.\n")
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print(f"\n{agent.name}: Goodbye! Have a great day!")
            break
        
        # Process the input and get a response
        try:
            response = agent.process_input(user_input)
            print(f"\n{agent.name}: {response}\n")
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            print(f"\n{agent.name}: I encountered an error while processing your request. Please try again.\n")


if __name__ == "__main__":
    main()
