"""
Helper utilities for OpenAgents framework.
"""
import json
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """Safely parse JSON string
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed JSON object, or empty dict if parsing fails
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return {}


def format_tool_calls(tool_calls: List[Dict[str, Any]]) -> str:
    """Format tool calls for display
    
    Args:
        tool_calls: List of tool calls
        
    Returns:
        Formatted string
    """
    result = []
    for i, call in enumerate(tool_calls):
        result.append(f"Tool Call #{i+1}:")
        result.append(f"  Name: {call.get('name', 'unknown')}")
        result.append(f"  Arguments: {json.dumps(call.get('arguments', {}), indent=2)}")
    
    return "\n".join(result)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def get_memory_usage() -> Dict[str, float]:
    """Get current memory usage
    
    Returns:
        Dictionary with memory usage information
    """
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # RSS in MB
            "vms_mb": memory_info.vms / 1024 / 1024   # VMS in MB
        }
    except ImportError:
        logger.warning("psutil not installed. Cannot get memory usage.")
        return {"error": "psutil not installed"}
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        return {"error": str(e)}


def result_to_markdown(result: Any) -> str:
    """Convert a result to markdown format
    
    Args:
        result: Result to convert
        
    Returns:
        Markdown-formatted string
    """
    if isinstance(result, dict):
        return json.dumps(result, indent=2)
    elif isinstance(result, list):
        return json.dumps(result, indent=2)
    else:
        return str(result)
