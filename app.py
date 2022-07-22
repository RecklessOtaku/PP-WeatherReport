from flask import Flask, render_template, request
from funcs import current_weather, weather_forecast, icon_selector


app = Flask(__name__)


# Home page of web application
@app.route("/")
def index():
    return render_template("index.html")


# Page for user to provide location name in order to get current weather
@app.route("/current", methods=["POST", "GET"])
def current():
    return render_template("current.html")


# Page for displaying current weather report
@app.route("/current_result", methods=["POST", "GET"])
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
def forecast():
    return render_template("forecast.html")


# Page for displaying weather forecast
@app.route("/forecast_result", methods=["POST", "GET"])
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
def contact():
    return render_template("contact.html")


# Page which is displayed when user encounters "Not Found" error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Page which is displayed when user encounters "Internal Server Error" error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# Running web application
if __name__ == "__main__":
    app.run()
