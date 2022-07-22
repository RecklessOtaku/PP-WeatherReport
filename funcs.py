from requests import get
from geopy import Nominatim
from geopy.exc import GeopyError
from collections import Counter


# OpenWeatherMap API key
KEY = "981542aa23cce064ff88f9ca9449e67c"
# OpenWeatherMap current weather API url
CUR = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
# OpenWeatherMap weather forecast API url
FOR = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

# Used to convert defaul temperature units (Fahrenheit) to Celsius
FAH = 273.15


def avg(values: list):
    """
    Returns average value of the list
    """

    return round(sum(values) / len(values))


def location_coordinates(location: str):
    """
    Converts location name to geographical coordinates
    """

    try:
        geolocator = Nominatim(user_agent="weather")
        location = geolocator.geocode(location)

        return location.latitude, location.longitude

    except GeopyError as E:
        return f"Something wrong with geolocation module: {E}"


def icon_selector(state: str):
    """
    Returns path to specific icon that fits provided weather state
    """

    selector = {
        "Thunderstorm": "static/icons/thunder.png",
        "Drizzle": "static/icons/rain.png",
        "Rain": "static/icons/rain.png",
        "Snow": "static/icons/snow.png",
        "Clear": "static/icons/clear.png",
        "Clouds": "static/icons/clouds.png",
    }
    if state in selector.keys():
        return selector[state]
    else:
        return selector["Clouds"]


def current_weather(location: str):
    """
    Makes API call to get current weather and returns response as a dictionary
    """

    # Convert provided location name to geographical coordinates
    coordinates = location_coordinates(location)
    lat, lon = coordinates[0], coordinates[1]

    # Make API call using coordinates as request headers
    response = get(CUR.format(lat, lon, KEY))

    # Check whether API responded succesfully or not
    if response.status_code == 200:
        # Convert response to json for further parsing
        data = response.json()

        # Pull out the most important parts of the response
        results = {
            "description": data["weather"][0]["main"].title(),
            "temperature": str(round(data["main"]["temp"] - 273.15)) + "C",
            "humidity": str(data["main"]["humidity"]) + "%",
            "wind": str(data["wind"]["speed"]) + "m/s",
        }

        return results
    else:
        return f"Something wrong with weather API: {response.status_code}"


def weather_forecast(location: str):
    """
    Makes API call to get weather forecast and returns response as a dictionary
    """

    coords = location_coordinates(location)
    lat, lon = coords[0], coords[1]

    response = get(FOR.format(lat, lon, KEY))
    if response.status_code == 200:
        data = response.json()

        # Get a list of days
        days = []
        for el in data["list"]:
            days.append(el["dt_txt"][:10])
        # Sort this list in increasing order
        days = sorted(set(days))

        # Create some dictionaries to store future parsing results
        temp = {day: [] for day in days}
        wind = {day: [] for day in days}
        humidity = {day: [] for day in days}
        des = {day: [] for day in days}

        # Parse each record in API response
        for el in data["list"]:
            # Associate values with concurrent record in days list
            if el["dt_txt"][:10] in days:
                # At this point we have dict[key: list[values]] structure
                temp[el["dt_txt"][:10]].append(round(el["main"]["temp"] - FAH))
                wind[el["dt_txt"][:10]].append(el["wind"]["speed"])
                humidity[el["dt_txt"][:10]].append(el["main"]["humidity"])
                des[el["dt_txt"][:10]].append(el["weather"][0]["main"])

        # To simplify things we get average value for each list of values
        temp = [str(round(avg(value))) + "C" for _, value in temp.items()]
        wind = [str(avg(value)) + "m/s" for _, value in wind.items()]
        humidity = [str(avg(value)) + "%" for _, value in humidity.items()]
        des = [Counter(value).most_common(1)[0][0] for _, value in des.items()]
        icons = [icon_selector(weather) for weather in des]

        # Compose resulting dictionary
        values = zip(temp, wind, humidity, des, icons)
        results = {day: value for day, value in zip(days, values)}

        return results
    else:
        return f"Something wrong with weather API: {response.status_code}"
