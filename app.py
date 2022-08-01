from flask import Flask, render_template, request
from funcs import current_weather, weather_forecast, icon_selector
from flask_caching import Cache
from random import randint


config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


# Home page of web application
@app.route("/")
@cache.cached(timeout=80)
def index():
    cities_file_path = "PP-WeatherReport\\static\\cities.txt"
    with open(cities_file_path, "r", encoding="utf-8") as cities_file:
        cities = cities_file.readlines()
        random_city = cities[randint(0, len(cities) - 1)]
        random_city = random_city.replace("\n", "").split(sep=", ")

        random_weather = current_weather(random_city[0])
        description = random_weather["description"]
        icon = icon_selector(description)
        temperature = random_weather["temperature"]
        humidity = random_weather["humidity"]
        wind = random_weather["wind"]

    return render_template(
        "index.html",
        place=", ".join(random_city),
        icon=icon,
        desc=description,
        temp=temperature,
        humid=humidity,
        wind=wind,
    )


# Page for user to provide location name in order to get current weather
@app.route("/current", methods=["POST", "GET"])
@cache.cached(timeout=80)
def current():
    return render_template("current.html")


# Page for displaying current weather report
@app.route("/current_result", methods=["POST", "GET"])
@cache.cached(timeout=80)
def current_result():
    # Reading user input using web form's name
    place = request.form["location"]
    weather = current_weather(place)

    description = weather["description"]
    icon = icon_selector(description)
    temperature = weather["temperature"]
    humidity = weather["humidity"]
    wind = weather["wind"]

    # Providing Jinja in-html variables with actual values
    return render_template(
        "current_result.html",
        place=place.title(),
        desc=description,
        icon=icon,
        temp=temperature,
        humid=humidity,
        wind=wind,
    )


# Page for user to provide location name in order to get weather forecast
@app.route("/forecast", methods=["POST", "GET"])
@cache.cached(timeout=80)
def forecast():
    return render_template("forecast.html")


# Page for displaying weather forecast
@app.route("/forecast_result", methods=["POST", "GET"])
@cache.cached(timeout=80)
def forecast_result():
    place = request.form["location"]
    data = weather_forecast(place)

    return render_template(
        "forecast_result.html",
        place=place.title(),
        data=data,
        )


# Page for user to contact application's author or view application's code
@app.route("/contact")
@cache.cached(timeout=80)
def contact():
    return render_template("contact.html")


# Page which is displayed when user encounters "Not Found" error
@app.errorhandler(404)
@cache.cached(timeout=80)
def page_not_found(e):
    return render_template("404.html"), 404


# Page which is displayed when user encounters "Internal Server Error" error
@app.errorhandler(500)
@cache.cached(timeout=80)
def internal_server_error(e):
    return render_template("500.html"), 500


# Running web application
if __name__ == "__main__":
    app.run()
