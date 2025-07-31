from typing import Optional

from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from langgraph.graph import CompiledStateGraph

try:
    from IPython.display import Markdown, display
except ImportError:
    # Fallback if not in Jupyter environment
    def display(content):
        print(content)

    class Markdown:
        def __init__(self, text):
            self.text = text

        def __str__(self):
            return self.text


def format_tools_description(tools: list[BaseTool]) -> str:
    return "\n\n".join(
        [
            f"- {tool.name}: {tool.description}\n Input arguments: {tool.args}"
            for tool in tools
        ]
    )


async def print_stream(app: CompiledStateGraph, input: str) -> Optional[BaseMessage]:
    display(Markdown("## New research running"))
    display(Markdown(f"### Input:\n\n{input}\n\n"))
    display(Markdown("### Stream:\n\n"))

    # Stream the results
    all_messages = []
    async for chunk in app.astream({"messages": [input]}, stream_mode="updates"):
        for updates in chunk.values():
            if messages := updates.get("messages"):
                all_messages.extend(messages)
                for message in messages:
                    message.pretty_print()
                    print("\n\n")

    # Return the last message if any
    if not all_messages:
        return None
    return all_messages[-1]
