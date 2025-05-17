"""
General purpose tools for OpenAgents framework.
"""
import math
import datetime
import random
from typing import List, Dict, Any, Optional

from openagents.tools.base import Tool, BaseToolProvider


class GeneralTools(BaseToolProvider):
    """Provider of general purpose tools"""
    
    def get_tools(self) -> List[Tool]:
        """Get all general purpose tools
        
        Returns:
            List of general purpose tools
        """
        return [
            Tool(
                name="calculator",
                description="Evaluate a mathematical expression",
                function=self.calculate
            ),
            Tool(
                name="get_current_time",
                description="Get the current date and time",
                function=self.get_current_time
            ),
            Tool(
                name="search_wikipedia",
                description="Search Wikipedia for information (simulated)",
                function=self.search_wikipedia
            ),
            Tool(
                name="get_weather",
                description="Get weather information for a location (simulated)",
                function=self.get_weather
            ),
            Tool(
                name="generate_random_number",
                description="Generate a random number within a range",
                function=self.generate_random_number
            )
        ]
    
    def calculate(self, expression: str) -> str:
        """Calculate the result of a mathematical expression
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Result of the calculation
        """
        # Create a safe namespace with only mathematical functions
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'len': len,
            'int': int,
            'float': float,
            'pow': pow,
            'math': math
        }
        
        # Add all math module functions
        for name in dir(math):
            if not name.startswith('_'):
                safe_dict[name] = getattr(math, name)
        
        try:
            # Evaluate the expression in the safe namespace
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    def get_current_time(self, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get the current date and time
        
        Args:
            format: Format string for the date and time
            
        Returns:
            Current date and time
        """
        return datetime.datetime.now().strftime(format)
    
    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for information (simulated)
        
        Args:
            query: Search query
            
        Returns:
            Simulated search results
        """
        return f"Results for '{query}' (simulated Wikipedia search):\n" + \
               f"This is a simulated response for demonstration purposes. " + \
               f"In a real implementation, this would connect to Wikipedia's API."
    
    def get_weather(self, location: str, unit: str = "celsius") -> str:
        """Get weather information for a location (simulated)
        
        Args:
            location: Location to get weather for
            unit: Temperature unit ('celsius' or 'fahrenheit')
            
        Returns:
            Simulated weather information
        """
        # Simulate weather data
        temp = random.randint(0, 30)
        if unit.lower() == "fahrenheit":
            temp = temp * 9/5 + 32
        
        conditions = random.choice([
            "Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Snowy", "Windy"
        ])
        
        return f"Weather in {location} (simulated): {temp}°{unit[0].upper()}, {conditions}"
    
    def generate_random_number(self, min_value: int = 1, max_value: int = 100) -> str:
        """Generate a random number within a range
        
        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
            
        Returns:
            Random number within the specified range
        """
        if min_value > max_value:
            return f"Error: min_value ({min_value}) cannot be greater than max_value ({max_value})"
        
        number = random.randint(min_value, max_value)
        return f"Random number between {min_value} and {max_value}: {number}"
