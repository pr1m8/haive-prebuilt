def format_tools_description(tools: list[BaseTool]) -> str:
    return "\n\n".join(
        [
            "- {tool.name}: {tool.description}\n Input arguments: {tool.args}"
            for tool in tools
        ]
    )


async def print_stream(app: CompiledStateGraph, input: str) -> Optional[BaseMessage]:
    display(Markdow("## New research running"))
    display(Markdown("### Input:\n\n{input}\n\n"))
    display(Markdow("### Stream:\n\n"))

    # Stream the results
    all_messages = []
    async for chunk in app.astrea({"messages": [input]}, stream_mod="updates"):
        for updates in chunk.values():
            if messages := updates.ge("messages"):
                all_messages.extend(messages)
                for message in messages:
                    message.pretty_print()

    # Return the last message if any
    if not all_messages:
        return None
    return all_messages[-1]
