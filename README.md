# Telegram Bot
[Python 3.13.7](https://www.python.org/downloads/release/python-3137/)
## To use:
1. Install [Python 3.13.7](https://www.python.org/downloads/release/python-3137/)
2. Create a virtual environment
```
python -m venv .venv
# Activate
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```
3. Download libraries
```shell
pip install -r requirements.txt
```
4. Generate API and bot token

[Telegram token](https://t.me/BotFather)

[Weather API](https://home.openweathermap.org/api_keys)

[Currency API](https://api.currencyfreaks.com/latest)

5. Create a `.env` file and specify your API there
```
# .env file
BOT_TOKEN=YOUR_TOKEN_TELEGRAM_BOT
WEATHER_API=YOUR_API_WEATHER
CURRENCY_API=YOUR_API_CURRENCY
```
6. Launch the bot!
```shell
python bot.py
```

A simple Telegram bot written in [Python 3.13.7](https://www.python.org/downloads/release/python-3137/) that provides:
- **Weather information** 🌦️  
- **Currency conversion** 💱    


## Features

### 🌥️ **Weather (/weather)**
- Type a city name (e.g. `Kyiv`, `London`) and get current weather details. 
- Data is fetched from the [OpenWeatherMap API](https://openweathermap.org/api)
- Example: `/weather Kyiv`

### 💱 **Currency Conversion (/convert)**
- Convert between different currencies with the `/convert` command  
- Example: `/convert 100 USD UAH`  
- Uses exchange rate API for real-time data



## Project Structure
```
telegram-bot/
│
├── bot.py # Main bot logic
├── config.py # API URLs and constants
├── .env # Environment variables
└── requirements.txt # Project dependencies

telegram-bot/services/
│
├── currency.py # Currency Conversion (API)
├── weather.py # Weather (API)
```