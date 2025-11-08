import requests
import os
from dotenv import load_dotenv

from config import CURRENCY_API_URL

# Load API from .env
load_dotenv()
CURRENCY_API_KEY = os.getenv("CURRENCY_API")


def parse_conversion_command(raw: str):
    if not raw:
        return None, None, None

    parts = raw.strip().split()

    # Handle various possible formats of user input
    if len(parts) == 1:
        # Example: "100usd" (missing target currency)
        return None, None, None
    elif len(parts) == 2:
        # If currencies are not written in capital letters, correct them
        num_part = ''.join([ch for ch in parts[0] if ch.isdigit() or ch == '.'])
        curr_from = ''.join([ch for ch in parts[0] if ch.isalpha()]).upper()
        curr_to = parts[1].upper()
    elif len(parts) == 3:
        num_part, curr_from, curr_to = parts
        curr_from, curr_to = curr_from.upper(), curr_to.upper()
    else:
        # Invalid input (too many parts)
        return None, None, None

    # Сonverting the numeric part into a float
    try:
        amount = float(num_part)
    except ValueError:
        amount = None
    # Returning values
    return amount, curr_from, curr_to


def convert_currency(raw: str) -> str:
    # Parse user input
    amount, curr_from, curr_to = parse_conversion_command(raw)
    if not amount or not curr_from or not curr_to:
        return "❌ Invalid format. Use: `/convert 10000 UAH USD`"

    # Ensure API key is available
    if not CURRENCY_API_KEY:
        return "❌ Currency API key not found. Please set CURRENCY_API_KEY in .env"

    # Prepare API request parameters
    params = {
        "apikey": CURRENCY_API_KEY,
        "symbols": f"{curr_from},{curr_to}"
    }

    try:
        # Send request to currency API
        resp = requests.get(CURRENCY_API_URL, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        # Handle connection or API errors
        return f"❌ Error contacting currency API: {e}"

    # Parse JSON response
    data = resp.json()
    rates = data.get("rates", {})

    # Validate that both currencies exist in the response
    if curr_from not in rates or curr_to not in rates:
        return f"❌ Could not find exchange rate for {curr_from} or {curr_to}"

    try:
        # API returns all rates relative to USD
        usd_to_from = float(rates[curr_from])
        usd_to_to = float(rates[curr_to])

        # Convert using USD as the intermediary currency
        converted = (usd_to_to / usd_to_from) * amount
    except (ValueError, ZeroDivisionError):
        return "❌ Conversion error"

    # Calculate direct conversion rate
    rate = usd_to_to / usd_to_from

    # Format the output message
    return (
        "Currency Conversion\n"
        f"{amount} {curr_from} = {round(converted, 2)} {curr_to}\n"
        f"1 {curr_from} = {round(rate, 4)} {curr_to}"
    )
