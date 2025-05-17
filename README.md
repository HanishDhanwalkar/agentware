# Agentware: A Minimal AI Agent Framework

Agentware is a lightweight Python framework designed to help you build AI agents with tool-calling capabilities. It provides the core components for creating agents that can interact with Large Language Models (LLMs) and utilize external tools to perform tasks.

## Key Features

* **Tool Registry:** Define and manage tools (functions) that your agents can use.  The framework helps convert your function definitions into a format suitable for LLM function calling.
* **LLM Client:** A simple interface for interacting with LLM APIs (currently designed for OpenAI, but can be extended).
* **Agent Architecture:** A base agent class to manage conversation history, state, and tool execution.
* **Extensibility:** The framework is designed to be extensible, allowing you to easily add new tools, LLM integrations, and agent functionalities.

## Getting Started

### Installation

1.  **Prerequisites:**
    * Python 3.7+
    * LLM of your choice - OpenAI models, Ollama models preffered
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/HanishDhanwalkar/agentware
    cd agentware
    ```
### Usage

1.  **Set up your LLM API key:**
    ```python
    import os
    os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"  # Replace with your actual API key
    ```
    Or, you can set it as an environment variable:
    ```bash
    export OPENAI_API_KEY="YOUR_API_KEY"
    ```
2.  **Define your tools:**
    ```python
    def search_web(query: str) -> str:
        """Simulate web search"""
        return f"Results for '{query}': [Simulated web search results]"
    
    def calculate(expression: str) -> str:
        """Calculate mathematical expression"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    # Create tool registry and register tools
    registry = ToolRegistry()
    registry.register_tool(Tool(
        name="search_web",
        description="Search the web for information",
        function=search_web
    ))
    registry.register_tool(Tool(
        name="calculate",
        description="Calculate mathematical expressions",
        function=calculate
    ))
    ```
    
3.  **Create and run an agent:**
    ```python
    from agentware import Agent, LLMClient, ToolRegistry, Tool # Import the necessary classes
    
    # Create LLM client
    llm = LLMClient(model="gpt-3.5-turbo")  # or gpt-4, etc.
    
    # Create agent
    agent = Agent(
        name="Assistant",
        system_prompt="You are a helpful assistant with access to tools. Use them when appropriate.",
        llm_client=llm,
        tool_registry=registry
    )
    
    # Run a conversation
    print("Agent: Hello! I'm your AI assistant. I can help you with various tasks.")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        response = agent.process_input(user_input)
        print(f"Agent: {response}")
    ```

## Contributing

Agentware is an open-source project, and contributions are welcome!  If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Write tests to ensure your changes work correctly.
5.  Submit a pull request.

## License

MIT License

## Acknowledgements

* This project is inspired by the work on LLM agents and tool usage.

##  Modules

### agentware.py
Contains the core classes for building agents:
* `Tool`:  Represents a tool that can be called by an agent
* `ToolRegistry`:  Manages the registration and retrieval of tools.
* `LLMClient`:  Handles communication with the LLM.
* `AgentState`:  Represents the state of the agent
* `Agent`:  The base agent class with tool-calling capabilities.

## Code Examples
### Defining a Tool
```python
def get_current_date() -> str:
    """Returns the current date"""
    from datetime import date
    today = date.today()
    return today.strftime("%Y-%m-%d")

date_tool = Tool(
    name="get_current_date",
    description="Gets the current date",
    function=get_current_date
)
Registering a Toolregistry = ToolRegistry()
registry.register_tool(date_tool)
Creating an Agentllm_client = LLMClient()
agent = Agent(
    name="DateAgent",
    system_prompt="You are a helpful agent that can get the current date.",
    llm_client=llm_client,
    tool_registry=registry
)
