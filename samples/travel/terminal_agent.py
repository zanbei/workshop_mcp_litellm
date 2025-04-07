from dotenv import load_dotenv
import genpilot as gp
import json
import asyncio

load_dotenv()

terminal = gp.TerminalChat()

def final_answer(answer_content):
    """111 This function is called when the final answer is obtained. The provided content represents the solution to the latest task or problem.

    Parameters:
        answer_content (str): The final answer content for the latest task or problem."""
    return answer_content

# def get_weather(location: str, time: str) -> str:

#     """Get the current weather in a given location. Location MUST be a city.
#     Parameters:
#     - location (str): The city name.
#     - time (str): Optional, defaults to "now".
    
#     Returns:
#         str: JSON-formatted temperature information."""
    
#     print(f"Fetching weather for {location} at {time}")
#     return json.dumps({"location": location, "temperature": "65", "time": time})

def get_weather(location: str, time: str = 'Now') -> str:
    """
    Get weather function that provides weather data for cities.

    Args:
        location (str): City name 
        time (str, optional): Time parameter 

    Returns:
        str: JSON string with weather data
    """
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
                "time": time or "current"
            })

        data = weather_data[location]
        print(f"Fetching weather for {location} at {time or 'current'}")
        response = {
            "location": location,
            "temperature": data["temperature"],
            "description": data["description"],
            "time": time or "current"
        }

        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "error": "Internal error occurred",
            "location": location,
            "time": time or "current"
        })

weather_observer = gp.Agent(
    name="Weather Observer",
    model_config={
        "name": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "config": {"stream": False},
    },
    chat=terminal,
    tools=[get_weather],
    description="I can get weather conditions for a city.",
    # system="Your role focuses on retrieving and analyzing current weather conditions for a specified city. Your Responsibilities: Use the get_weather tool to find temperature. Typically, you only call the tool once and return the result. Do not call the weather with same input many times",
    system="""MUST use the get_weather tool to check weather conditions.
    DEBUG: Always print the tool response before returning it.
    DEBUG: If you receive this message, respond with 'Weather Observer Ready"""
)
def get_fashion_advice(location: str, temperature: str) -> str:
    """
    Provide fashion advice based on location and temperature.

    Parameters:
        location (str): City name (Copenhagen/Beijing/Berlin/Paris/Phuket/Shanghai)
        temperature (str): Temperature information, e.g., "20°C"

    Returns:
        str: JSON-formatted clothing advice
    """
    import json

    # Parse temperature
    temp_value = float(temperature.replace("°C", ""))

    # Basic advice based on temperature
    if temp_value < 10:
        base_clothing = {
            "Coat": "Thick coat or down jacket",
            "Top": "Warm sweater or high-neck knitwear",
            "Bottom": "Warm trousers",
            "Accessories": "Scarf, hat, and gloves",
            "Shoes": "Waterproof and warm boots"
        }
    elif temp_value < 20:
        base_clothing = {
            "Coat": "Light jacket or windbreaker",
            "Top": "Long-sleeved shirt or sweater",
            "Bottom": "Casual trousers",
            "Accessories": "Scarf (may be needed in the morning and evening)",
            "Shoes": "Comfortable sneakers or casual shoes"
        }
    else:
        base_clothing = {
            "Coat": "Optional lightweight sun protection jacket",
            "Top": "Short-sleeved or lightweight long-sleeved",
            "Bottom": "Lightweight trousers or shorts",
            "Accessories": "Sun hat and sunglasses",
            "Shoes": "Sandals or breathable sneakers"
        }

    # City-specific advice
    city_specific = {
        "Copenhagen": {
            "City Characteristics": "Nordic fashion capital, minimalist style",
            "Dressing Style": "Simple and elegant, mainly black, white, and gray",
            "Cultural Advice": "Conservative attire, emphasizing environmental awareness",
            "Special Tips": "Weather can be unpredictable; bring rain gear",
            "Suitable Venues": "Design Museum, Nyhavn, The Little Mermaid",
            "Taboos": "Avoid overly flashy outfits"
        },
        "Beijing": {
            "City Characteristics": "Modern and traditional international metropolis",
            "Dressing Style": "Elegant and practical",
            "Cultural Advice": "Dress formally when visiting attractions",
            "Special Tips": "Pay attention to air quality; prepare masks",
            "Suitable Venues": "Forbidden City, Great Wall, Hutongs",
            "Taboos": "Avoid revealing attire when visiting temples"
        },
        "Berlin": {
            "City Characteristics": "Fusion of avant-garde art and historical culture",
            "Dressing Style": "Individualized, street style is popular",
            "Cultural Advice": "Dress can be bold and innovative",
            "Special Tips": "Large temperature differences in spring and autumn; layer clothing",
            "Suitable Venues": "Museum Island, Brandenburg Gate, East Side Gallery",
            "Taboos": "Avoid inappropriate attire when visiting memorials"
        },
        "Paris": {
            "City Characteristics": "Global fashion capital",
            "Dressing Style": "Elegant and fashionable, emphasizing details",
            "Cultural Advice": "Lean towards formal elegance",
            "Special Tips": "High-end restaurants require formal attire",
            "Suitable Venues": "Eiffel Tower, Louvre, Champs-Élysées",
            "Taboos": "Avoid athletic wear in formal settings"
        },
        "Phuket": {
            "City Characteristics": "Tropical island resort",
            "Dressing Style": "Light and cool, vacation style",
            "Cultural Advice": "Be mindful of Thai cultural etiquette",
            "Special Tips": "Sunscreen and insect repellent are essential",
            "Suitable Venues": "Beaches, temples, night markets",
            "Taboos": "Dress appropriately when visiting temples"
        },
        "Shanghai": {
            "City Characteristics": "Modern international metropolis",
            "Dressing Style": "Fashionable and avant-garde, blending Eastern and Western elements",
            "Cultural Advice": "Dress can be fashionable and bold",
            "Special Tips": "Carry rain gear and check weather forecasts",
            "Suitable Venues": "The Bund, Yu Garden, Tianzifang",
            "Taboos": "Avoid overly casual attire in special occasions"
        }
    }

    # Get city-specific information
    city_info = city_specific.get(location, {
        "City Characteristics": "Please check local characteristics",
        "Dressing Style": "Suggest checking local dressing habits",
        "Cultural Advice": "Be mindful of local culture",
        "Special Tips": "Suggest checking local weather forecasts",
        "Suitable Venues": "Please check local tourist information",
        "Taboos": "Be mindful of dressing appropriately"
    })

    # Combine response
    response = {
        "Location": location,
        "Temperature": temperature,
        "Basic Clothing Advice": base_clothing,
        "City-Specific Advice": city_info,
        "Weather Reminder": f"Current temperature {temperature}, " + (
            "Pay attention to keeping warm" if temp_value < 10 else
            "Temperature is moderate" if temp_value < 20 else
            "Pay attention to sun protection and cooling"
        )
    }

    return json.dumps(response, ensure_ascii=False, indent=2)

advisor = gp.Agent(
    name="Local Advisor",
    model_config={
        "name": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "config": {
            "max_tokens": 1500,
        },
    },
    chat=terminal,
    description="Provides fashion and cultural advice",
    system="""MUST use the get_fashion_advice tool to check local fashion trends.
    DEBUG: Always print the tool response before returning it.
    Considerations:
    1. Local fashion trends
    2. Weather conditions
    3. Cultural appropriateness
    4. Seasonal advice
    Please provide suggestions in English""",
    tools=[get_fashion_advice],
)

traveller = gp.Agent(
    name="Traveller",
    model_config={
        "name": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "config": {"stream": False},
    },
    chat=terminal,
    handoffs=[weather_observer, advisor],
    system="This managerial role combines insights from both the Weather Observer and the Advisor to recommend appropriate clothing choices. Once you have the information for both Observer and Advisor. The final response with concise, straightforward items, like 1,2,3.. ",
    max_iter=20,
    memory=gp.memory.BufferMemory(30),
)


def get_user_destination():
    """Get the user's desired destination"""
    suggested_cities = ["Copenhagen", "Beijing", "Berlin", "Paris", "Phuket", "Shanghai"]
    print("Welcome to the travel assistant!")
    print(f"Recommended cities: {', '.join(suggested_cities)}")
    print("Please enter the city you want to visit (you can also enter other cities):")
    
    while True:
        destination = input().strip()
        if destination:  # Simple input validation
            return destination
        print("Please enter a valid destination name")

if __name__ == "__main__":
    # Get the user's input destination
    destination = get_user_destination()
    
    # Construct the initial message and start the conversation
    initial_message = f"I want to travel to {destination} tomorrow, please give me some suggestions."
    message = asyncio.run(traveller(initial_message))
    
    # # Print the result
    # print("\nTravel assistant's suggestions:")
    # print(message)