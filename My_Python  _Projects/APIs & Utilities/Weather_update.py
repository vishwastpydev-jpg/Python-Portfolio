import requests
from plyer import notification

# Helper function to map Open-Meteo codes to readable descriptions
def get_weather_desc(code):
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
        61: "Slight rain", 71: "Slight snow", 95: "Thunderstorm"
    }
    return codes.get(code, "Cloudy")

# --- USER INPUT SECTION ---
city = input("Enter the city name: ").strip()

# 1. Get coordinates from city name
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": city, "count": 1}

try:
    geo_res = requests.get(geo_url, params=geo_params).json()

    if "results" in geo_res:
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        full_city_name = geo_res["results"][0]["name"]
        country = geo_res["results"][0].get("country", "")

        # 2. Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        weather_res = requests.get(weather_url, params=weather_params).json()

        if "current_weather" in weather_res:
            current = weather_res["current_weather"]
            temp = current["temperature"]
            wind = current["windspeed"]
            condition = get_weather_desc(current["weathercode"])
            
            weather_info = f"Condition: {condition}\nTemp: {temp}°C | Wind: {wind} km/h"

            print(f"\n--- Weather in {full_city_name}, {country} ---")
            print(weather_info)

            # 3. Cross-platform notification
            notification.notify(
                title=f"Weather Update: {full_city_name}",
                message=weather_info,
                app_icon=None,  # e.g. 'path/to/icon.ico' on Windows
                timeout=10
            )
        else:
            print("Error: Could not retrieve weather data.")
    else:
        print(f"Error: City '{city}' not found.")

except requests.exceptions.ConnectionError:
    print("Error: Please check your internet connection.")