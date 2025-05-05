from mcp.server.fastmcp import FastMCP
import json
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    # """Get weather for location."""
    # return "Beijing \n Weather: Sunny\n Temperature: 25°C\n Humidity: 60%\n Wind Speed: 10 km/h\n"
    # Mock weather data for specific cities
    weather_data = {
        "Copenhagen": {"temperature": "18", "description": "Partly cloudy"},
        "Beijing": {"temperature": "25", "description": "Sunny"},
        "Berlin": {"temperature": "20", "description": "Clear sky"},
        "Paris": {"temperature": "22", "description": "Cloudy"},
        "Phuket": {"temperature": "32", "description": "Tropical"},
        "Shanghai": {"temperature": "28", "description": "Humid"}
    }

    try:
        if location not in weather_data:
            return json.dumps({
                "error": f"No weather data available for {location}. Available cities: {', '.join(weather_data.keys())}",
                "location": location,
            })

        data = weather_data[location]
        response = {
            "location": location,
            "temperature": data["temperature"],
            "description": data["description"],
        }

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "error": f"An error occurred: {str(e)}",
            "location": location,
        })

if __name__ == "__main__":
    mcp.run(transport="sse")
