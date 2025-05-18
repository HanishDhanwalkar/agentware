"""
Basic example of using the OpenAgents framework.
"""
import logging
import sys
import os
import termcolor

# Add the parent directory to sys.path to allow importing the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openagents import create_agent

def main():
    """Run a basic example of the OpenAgents framework"""
    term_size = os.get_terminal_size()
    print('=' * term_size.columns)  
    
    try:
        agent = create_agent(
            name="MyAgent",
            system_prompt="You are a helpful AI assistant with access to tools. Use them when appropriate to provide accurate information.",
            # llm_model="llama3.2",
            llm_model="deepseek-r1:7b",
            verbose=True,
        )
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        
    # 
    print(f"\n{agent.name}: Hello! I'm your AI assistant. I can help you with various tasks using tools.")
    print("Type", termcolor.colored('exit', 'red'), "or", termcolor.colored('q', 'red'), "to end the conversation.\n")
    print('=' * term_size.columns)  
    print('=' * term_size.columns)  
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        print('=' * term_size.columns)  
        
        if user_input.lower() == "exit" or user_input.lower() == "q":
            print(f"\n{agent.name}: Goodbye! Have a great day!")
            print('=' * term_size.columns)  
            break
        
        # Process the input and get a response
        try:
            response = agent.process_input(user_input)
            print('=' * term_size.columns)  
            print(f"\n{agent.name}: {response}\n")
            print('=' * term_size.columns)  
            
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            print(f"\n{agent.name}: I encountered an error while processing your request. Please try again.\n")


if __name__ == "__main__":
    main()
