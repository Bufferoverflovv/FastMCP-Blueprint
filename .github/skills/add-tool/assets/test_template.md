# Tool Test Template

Placeholders to substitute before saving:

| Placeholder | Description |
|-------------|-------------|
| `TOOL_NAME` | Matches the tool function name exactly |
| `PARAM_NAME` | Primary parameter name used in the success test |
| `PARAM_VALUE` | Example value to pass in the success test |
| `EXPECTED` | Expected return value for the success test |

```python
async def test_TOOL_NAME_success(client):
    result = await client.call_tool("TOOL_NAME", {"PARAM_NAME": "PARAM_VALUE"})

    assert not result.is_error
    assert len(result.content) == 1
    # Adjust assertion to match actual return type:
    assert result.content[0].text == "EXPECTED"


async def test_TOOL_NAME_error_on_invalid_input(client):
    result = await client.call_tool("TOOL_NAME", {"PARAM_NAME": ""}, raise_on_error=False)

    assert result.is_error
```
