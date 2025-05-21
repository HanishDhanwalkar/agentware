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
    pip install -r requirements.txt
    ```
### Usage
TODO:

### Features
TODO:
1. Websurfer
2. PDF 
3. RAG tool
4. code agent (potential models: DeepseekCoder)
5. Project planner


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
* OLLAMA foundation

##  Modules

### agentware.py
Contains the core classes for building agents:
* `Tool`:  Represents a tool that can be called by an agent
* `ToolRegistry`:  Manages the registration and retrieval of tools.
* `LLMClient`:  Handles communication with the LLM.
* `AgentState`:  Represents the state of the agent
* `Agent`:  The base agent class with tool-calling capabilities.