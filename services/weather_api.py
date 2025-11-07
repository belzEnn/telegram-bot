import requests
from config import WEATHER_API_KEY, WEATHER_API_URL

def _sanitize_city(raw: str) -> str:
    # Clean up the user input (city name)
    # Remove extra spaces and return an empty string if input is invalid
    if not raw:
        return ""
    city = raw.strip()
    return city 


def get_weather(raw_city: str) -> str:
    # Convert raw input to a clean city name
    city = _sanitize_city(raw_city)
    if not city:
        return "❌ City name is empty. Please send a city name, e.g. `Kyiv`"

    # Check if API key is configured
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return "Weather API key is not configured"

    # Prepare query parameters for OpenWeatherMap API
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "en"
    }

    try:
        # Send request to weather API
        resp = requests.get(WEATHER_API_URL, params=params, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors
        status = getattr(resp, "status_code", None)
        if status == 401:
            return "Unauthorized (invalid weather API key)"
        if status == 404:
            return "🏙️ City not found. Try different spelling"
        return f"HTTP error: {http_err} (status {status})"
    except requests.RequestException as e:
        # Handle connection or timeout errors
        return f"Error while contacting weather service: {e}"

    # parse JSON response
    data = resp.json()
    if data.get("cod") and int(data.get("cod")) != 200:
        # Handle API-level errors (like invalid city)
        msg = data.get("message", "Unknown error")
        return f"API error: {msg}"

    # extract important data from JSON
    name = data.get("name", city)
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind = data.get("wind", {})

    # Read specific values with defaults
    temp = main.get("temp", "N/A")
    feels = main.get("feels_like", "N/A")
    humidity = main.get("humidity", "N/A")
    desc = weather.get("description", "").capitalize()
    wind_speed = wind.get("speed", "N/A")

    # Final message
    text = (
        f"*Weather in {name}*\n"
        f"Temperature: {temp}°C\n"
        f"Feels like: {feels}°C\n"
        f"Condition: {desc}\n"
        f"Humidity: {humidity}%\n"
        f"Wind speed: {wind_speed} m/s"
    )
    return text
