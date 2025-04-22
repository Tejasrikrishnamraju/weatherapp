import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Your OpenWeather API key
API_KEY = "4aac6b3fdc5a1e844d220bd1f4d5aa5a"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def get_weather():
    if request.method == "POST":
        # Get the city from the user's input
        city = request.form.get("city")
        
        if city:
            # Make API call
            response = requests.get(f"{BASE_URL}?q={city}&appid={API_KEY}")
            data = response.json()

            if response.status_code == 200:
                # Extract relevant weather details
                weather_details = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": round(data["main"]["temp"] - 273.15, 2),  # Convert Kelvin to Celsius
                    "feels_like": round(data["main"]["feels_like"] - 273.15, 2),
                    "weather_description": data["weather"][0]["description"].capitalize(),
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                }
                return render_template("weather.html", weather=weather_details)
            else:
                return f"Error: {data['message']}"
        else:
            return "Please enter a valid city name."
    return render_template("input.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

