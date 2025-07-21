from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP(name = "hello-mcp",stateless_http = True)

mcp_app = mcp.streamable_http_app()
# create weather tool
@mcp.tool()
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

# create a tool to get the time
@mcp.tool()
def get_time() -> str:
    return f"The time is {datetime.now().strftime('%H:%M:%S')}"

# create a tool to get the date