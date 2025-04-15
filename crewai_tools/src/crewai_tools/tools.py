from crewai.tools import BaseTool
from litellm import completion
import os
from pydantic import BaseModel, Field
import json
from dotenv import load_dotenv
load_dotenv()
from typing import Type, Optional, List, Dict, Any


class GetWeatherToolInput(BaseModel):
    location: str = Field(..., description="City name to get the weather for")
    date: str = Field(..., description="Date to get the weather for (YYYY-MM-DD)")

class GetWeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get the weather for a specific location and date."
    args_schema: Type[BaseModel] = GetWeatherToolInput

    def _run(self, location: str, date: str) -> str:
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
                    "date": date or "current"
                })

            data = weather_data[location]
            print(f"Fetching weather for {location} at {date or 'current'}")
            response = {
                "location": location,
                "temperature": data["temperature"],
                "description": data["description"],
                "date": date or "current"
            }

            return json.dumps(response, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "error": f"An error occurred: {str(e)}",
                "location": location,
                "date": date or "current"
            })


class GetFashionToolInput(BaseModel):
    location: str = Field(..., description=" City name (Copenhagen/Beijing/Berlin/Paris/Phuket/Shanghai)")
    weather: str = Field(..., description="Weather information, e.g., sunny, rainy, etc.")
    temperature: str = Field(..., description="Temperature in Celsius")

class GetFashionTool(BaseTool):
    name: str = "get_fashion"
    description: str = "Get the fashion from a specific location, weather and temperature."
    args_schema: Type[BaseModel] = GetFashionToolInput

    def _run(self, location: str, weather: str, temperature: str) -> str:
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


def get_tools():
    return [GetWeatherTool(),GetFashionTool()]