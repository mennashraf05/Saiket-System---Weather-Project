import sys
import requests
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

# Mapping weather codes to descriptions in English\N{WEATHER_CODES}
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
}


def get_coordinates(city: str, language: str = "en"):
    """
    Fetch latitude and longitude for a given city using Open-Meteo Geocoding API.
    """
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&language={language}&format=json"
    )
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"No coordinates found for '{city}'")
    res = data["results"][0]
    return res["latitude"], res["longitude"], res["name"], res.get("country")


def get_current_weather(lat: float, lon: float, temp_unit: str = "celsius"):
    """
    Fetch current weather from Open-Meteo.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&timezone=auto"
        f"&temperature_unit={temp_unit}"
        f"&windspeed_unit=kmh"
    )
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "current_weather" not in data:
        raise ValueError("No current weather data available")
    return data["current_weather"]


def get_weekly_forecast(lat: float, lon: float, temp_unit: str = "celsius"):
    """
    Fetch 7-day forecast from Open-Meteo.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&timezone=auto"
        f"&temperature_unit={temp_unit}"
    )
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if "daily" not in data:
        raise ValueError("No daily forecast data available")
    return data["daily"]


def display_current_weather(city_name: str, country: str, weather: dict, temp_unit: str):
    """
    Print the current weather information.
    """
    symbol = "°C" if temp_unit == "celsius" else "°F"
    temp = weather.get("temperature", "?")
    wind = weather.get("windspeed", "?")
    code = weather.get("weathercode", None)
    desc = WEATHER_CODES.get(code, f"Code {code}")

    print(f"Current weather in {city_name}, {country}:")
    print(f"  • Condition: {desc}")
    print(f"  • Temperature: {temp}{symbol}")
    print(f"  • Wind speed: {wind} km/h\n")


def display_weekly_forecast(city_name: str, country: str, daily: dict, temp_unit: str):
    """
    Print a 7-day forecast table.
    """
    symbol = "°C" if temp_unit == "celsius" else "°F"
    dates = daily["time"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    codes = daily["weathercode"]

    print(f"7-day forecast for {city_name}, {country}:")
    for date, tmax, tmin, code in zip(dates, max_temps, min_temps, codes):
        try:
            date_str = datetime.fromisoformat(date).strftime("%Y-%m-%d")
        except ValueError:
            date_str = date
        desc = WEATHER_CODES.get(code, f"Code {code}")
        print(f"{date_str} | Max: {tmax}{symbol} | Min: {tmin}{symbol} | {desc}")
    print()


def plot_weekly_forecast(city_name: str, country: str, daily: dict, temp_unit: str):
    """
    Plot the 7-day forecast using Matplotlib.
    """
    dates = [datetime.fromisoformat(d) for d in daily["time"]]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    symbol = "°C" if temp_unit == "celsius" else "°F"

    plt.figure()
    plt.plot(dates, max_temps, label=f"Max Temp ({symbol})")
    plt.plot(dates, min_temps, label=f"Min Temp ({symbol})")
    plt.title(f"7-Day Forecast for {city_name}, {country}")
    plt.xlabel("Date")
    plt.ylabel(f"Temperature ({symbol})")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch weather data for one or more cities via Open-Meteo"
    )
    parser.add_argument(
        "cities",
        nargs="+",
        help="One or more city names (e.g. Cairo London \"New York\")"
    )
    parser.add_argument(
        "--units",
        choices=["celsius", "fahrenheit"],
        default="celsius",
        help="Temperature unit (default: celsius)"
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Language for geocoding API (default: en)"
    )
    parser.add_argument(
        "--daily",
        action="store_true",
        help="Show 7-day forecast"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Plot 7-day forecast when --daily is used"
    )

    args = parser.parse_args()

    for city in args.cities:
        try:
            lat, lon, name, country = get_coordinates(city, language=args.lang)
            current = get_current_weather(lat, lon, temp_unit=args.units)
            display_current_weather(name, country or "Unknown", current, temp_unit=args.units)
            if args.daily:
                daily = get_weekly_forecast(lat, lon, temp_unit=args.units)
                display_weekly_forecast(name, country or "Unknown", daily, temp_unit=args.units)
                if args.plot:
                    plot_weekly_forecast(name, country or "Unknown", daily, temp_unit=args.units)
        except Exception as e:
            print(f"Error for {city}: {e}\n")

if __name__ == "__main__":
    main()
