

async def test_call_nonexistent_tool_returns_error(client):
    result = await client.call_tool("nonexistent_tool", {}, raise_on_error=False)

    assert result.is_error


async def test_tool_list_includes_hello_world(client):
    tools = await client.list_tools()
    tool_names = [t.name for t in tools]

    assert "hello_world" in tool_names
