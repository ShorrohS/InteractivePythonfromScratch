"""
Project 01 — Weather Dashboard
Phase 11: APIs

SKILLS PRACTICED:
  - HTTP GET requests with requests library
  - Parsing JSON responses
  - API authentication with API keys
  - Error handling for HTTP errors
  - Formatting and displaying data

SETUP:
  1. Get a free API key from: https://openweathermap.org/api
  2. Set your API key in the API_KEY variable below (or use environment variable)
  3. pip install requests

HOW TO RUN:
  python main.py
"""

import requests
import os
from datetime import datetime


# Get API key from environment variable (best practice) or set directly
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    return k - 273.15


def kelvin_to_fahrenheit(k: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return (k - 273.15) * 9/5 + 32


def get_weather(city: str) -> dict | None:
    """
    Fetch current weather for a city.
    Returns weather data dict or None on error.
    """
    params = {
        "q": city,
        "appid": API_KEY
    }
    
    try:
        response = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("❌ Error: Invalid API key. Get one free at openweathermap.org")
        elif response.status_code == 404:
            print(f"❌ Error: City '{city}' not found.")
        elif response.status_code == 429:
            print("❌ Error: API rate limit exceeded. Try again in a minute.")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    return None


def get_forecast(city: str) -> dict | None:
    """Fetch 5-day forecast for a city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "cnt": 5    # 5 time steps (each 3 hours)
    }
    
    try:
        response = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    
    return None


def display_current_weather(data: dict) -> None:
    """Display current weather in a formatted layout."""
    
    city = data["name"]
    country = data["sys"]["country"]
    temp_k = data["main"]["temp"]
    feels_like_k = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]
    visibility = data.get("visibility", 0) / 1000   # Convert to km
    
    temp_c = kelvin_to_celsius(temp_k)
    feels_c = kelvin_to_celsius(feels_like_k)
    temp_f = kelvin_to_fahrenheit(temp_k)
    
    # Sunrise/sunset
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
    
    print("=" * 55)
    print(f"  🌍 {city}, {country}")
    print(f"  📅 {datetime.now().strftime('%A, %B %d, %Y  %H:%M')}")
    print("=" * 55)
    print()
    print(f"  🌡️  Temperature:    {temp_c:.1f}°C / {temp_f:.1f}°F")
    print(f"  🤔 Feels Like:     {feels_c:.1f}°C")
    print(f"  ☁️  Condition:      {description}")
    print()
    print(f"  💧 Humidity:       {humidity}%")
    print(f"  🌬️  Wind Speed:     {wind_speed} m/s")
    print(f"  👁️  Visibility:     {visibility:.1f} km")
    print(f"  📊 Pressure:       {pressure} hPa")
    print()
    print(f"  🌅 Sunrise:        {sunrise}")
    print(f"  🌇 Sunset:         {sunset}")
    print("=" * 55)


def weather_advice(data: dict) -> str:
    """Generate practical advice based on weather."""
    temp_c = kelvin_to_celsius(data["main"]["temp"])
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].lower()
    
    advice = []
    
    if temp_c < 5:
        advice.append("🧥 Wear a heavy coat — it's very cold.")
    elif temp_c < 15:
        advice.append("🧣 Bring a jacket — it's chilly.")
    elif temp_c > 35:
        advice.append("☀️ Stay hydrated — it's very hot.")
    
    if "rain" in description or "drizzle" in description:
        advice.append("☂️ Bring an umbrella.")
    
    if "snow" in description:
        advice.append("❄️ Drive carefully — snow conditions.")
    
    if humidity > 80:
        advice.append("💦 High humidity — it will feel hotter.")
    
    if not advice:
        advice.append("✅ Conditions look good!")
    
    return "\n  ".join(advice)


def main():
    """Main weather dashboard."""
    
    print("=" * 55)
    print("    🌤️  PYTHON WEATHER DASHBOARD")
    print("=" * 55)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print()
        print("  ⚠️  Demo mode — no API key configured.")
        print()
        print("  To use real weather data:")
        print("  1. Sign up free at: https://openweathermap.org")
        print("  2. Get your API key")
        print("  3. Set: API_KEY = 'your_key_here' in this file")
        print("     OR set environment variable: OPENWEATHER_API_KEY")
        print()
        print("  Showing demo data instead...")
        
        # Demo data (what real data looks like)
        demo = {
            "name": "London",
            "sys": {"country": "GB", "sunrise": 1700000000, "sunset": 1700020000},
            "main": {"temp": 285.15, "feels_like": 283.15, "humidity": 78, "pressure": 1015},
            "weather": [{"description": "light rain", "icon": "10d"}],
            "wind": {"speed": 5.2},
            "visibility": 10000
        }
        print()
        display_current_weather(demo)
        print()
        print("  📌 ADVICE:")
        print(f"  {weather_advice(demo)}")
        return
    
    # Real API call
    while True:
        print()
        city = input("  Enter city name (or 'quit' to exit): ").strip()
        
        if city.lower() in ("quit", "q", "exit"):
            print("  Goodbye! ☀️")
            break
        
        if not city:
            continue
        
        print(f"\n  Fetching weather for {city}...")
        
        weather_data = get_weather(city)
        
        if weather_data:
            print()
            display_current_weather(weather_data)
            print()
            print("  📌 ADVICE:")
            print(f"  {weather_advice(weather_data)}")


if __name__ == "__main__":
    main()
