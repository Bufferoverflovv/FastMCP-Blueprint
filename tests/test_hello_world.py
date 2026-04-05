async def test_hello_world_returns_greeting(client):
    result = await client.call_tool("hello_world", {"name": "FastMCP"})

    assert len(result.content) == 1
    assert result.content[0].text == "Hello, FastMCP!"


async def test_hello_world_default_name(client):
    result = await client.call_tool("hello_world", {})

    assert len(result.content) == 1
    assert result.content[0].text == "Hello, World!"
