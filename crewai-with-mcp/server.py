from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "Beijing \n Weather: Sunny\n Temperature: 25°C\n Humidity: 60%\n Wind Speed: 10 km/h\n"

if __name__ == "__main__":
    mcp.run(transport="sse")
