"""
Package initialization for OpenAgents.

This module initializes the OpenAgents package and provides a simplified API.
"""
import logging
from typing import Dict, List, Any, Optional

# Set up package-level logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Import main components for easier access
from openagents.core.agent import Agent
from openagents.tools.registry import ToolRegistry
from openagents.tools.base import Tool
from openagents.llm.providers import LLMRegistry
from openagents.tools.general import GeneralTools

# Package version
__version__ = "0.1.0"


def create_agent(
    name: str,
    system_prompt: str,
    llm_provider: str = "ollama",
    llm_model: str = "llama3",
    include_general_tools: bool = True,
    verbose: bool = False,
    **kwargs
) -> Agent:
    """Create an agent with the specified configuration
    
    Args:
        name: Name of the agent
        system_prompt: System prompt for the agent
        llm_provider: LLM provider to use
        llm_model: LLM model to use
        include_general_tools: Whether to include general tools
        verbose: Whether to enable verbose logging
        **kwargs: Additional arguments to pass to the LLM provider
        
    Returns:
        Configured agent
    """
    # Create LLM
    llm_class = LLMRegistry.get_provider(llm_provider)
    llm = llm_class(model=llm_model, **kwargs)
    
    # Create tool registry
    registry = ToolRegistry()
    
    # Add general tools if requested
    if include_general_tools:
        registry.register_provider(GeneralTools())
    
    # Create and return agent
    return Agent(
        name=name,
        system_prompt=system_prompt,
        llm=llm,
        tool_registry=registry,
        verbose=verbose
    )
