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
args.add_argument(
    "--language", "-l", help="Default programming language", default="python"
)

args = args.parse_args()

from openagents import create_agent
from v1.tools import ToolRegistry

# Define coding-specific tools
tool_registry = ToolRegistry()

# Tool for analyzing code complexity
@tool_registry.register
def analyze_code_complexity(code: str, language: str = "python") -> str:
    """
    Analyzes the complexity of provided code.
    
    Args:
        code: The source code to analyze
        language: Programming language of the code
    
    Returns:
        A summary of code complexity metrics
    """
    # This would be implemented with actual code analysis libraries
    # For example, using radon for Python, or other language-specific tools
    return f"Analyzing {language} code complexity: [Placeholder for actual analysis]"

# Tool for suggesting code optimizations
@tool_registry.register
def suggest_optimizations(code: str, language: str = "python") -> str:
    """
    Suggests potential optimizations for the provided code.
    
    Args:
        code: The source code to optimize
        language: Programming language of the code
    
    Returns:
        A list of potential optimizations
    """
    # This would be implemented with code analysis libraries
    return f"Optimization suggestions for {language} code: [Placeholder for actual suggestions]"

# Tool for running unit tests
@tool_registry.register
def run_tests(code: str, test_code: str = None, language: str = "python") -> str:
    """
    Runs unit tests against the provided code.
    
    Args:
        code: The source code to test
        test_code: The test code (optional)
        language: Programming language of the code
    
    Returns:
        Test results
    """
    # This would be implemented with test runners
    return f"Test results for {language} code: [Placeholder for actual test results]"

# Create the coding agent with the specialized tools
coding_agent = create_agent(
    name="CodeAssistant",
    system_prompt=f"""You are an expert coding assistant specializing in software development.
You excel at writing clean, efficient code and helping debug issues.
Your primary language is {args.language}, but you can work with many programming languages.
When writing code:
- Prioritize readability and maintainability
- Include helpful comments
- Follow best practices for the language
- Explain your implementation decisions
You have specialized tools available to analyze code complexity, suggest optimizations, and run tests.""",
    llm_model=args.model,
    verbose=args.verbose,
    tools=tool_registry.get_tools()
)

# Process user inputs
print("CodeAssistant initialized. Enter your coding questions (type 'exit' to quit):")
while True:
    user_input = input("> ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    response = coding_agent.process_input(user_input)
    print("\n" + response + "\n")