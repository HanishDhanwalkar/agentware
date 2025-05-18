import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openagents import Agent, LLMClient, ToolRegistry, Tool


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
registry = ToolRegistry()
registry.register_tool(date_tool)
llm_client = LLMClient()

agent = Agent(
    name="DateAgent",
    system_prompt="You are a helpful agent that can get the current date.",
    llm_client=llm_client,
    tool_registry=registry
)
