from statistics import mean
from flask import Flask, request
from flask.templating import render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/result', methods=["POST"])
def show_forcast():
    try:
        city = request.form["city"]
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        if len(response.json()) == 1:
            raise ValueError("Location not found")
        latitude = list(response.json().values())[0][0].get('latitude')
        longitude = list(response.json().values())[0][0].get('longitude')
        country = list(response.json().values())[0][0].get('country')
        city = list(response.json().values())[0][0].get('name')
        weather_data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m")
    except ValueError:
        return render_template("error.html", title="Location not found", error_type="Location not found",
                               error_desc="Sorry, we couldn't find the location you were looking for. Please try again.")
    except:
        return render_template("error.html", title="Connection error", error_type="Connection Error",
                               error_desc="Sorry, we couldn't render the page due to connection error. Please try again.")
    list_of_times = list(weather_data.json()['hourly'].values())[0]
    list_of_weather = list(weather_data.json()['hourly'].values())[1]
    list_of_humidities = list(weather_data.json()['hourly'].values())[2]
    weather_dict = {}
    humidity_dict = {}
    for i, j, k in zip(list_of_times[7:], list_of_weather[7:], list_of_humidities[7:]):
        date, time = i.split('T')
        time = int(time[:2])
        humidity_dict[date] = humidity_dict.get(date, list()) + [k]
        if 7 <= time < 19:
            weather_dict[date + "day"] = weather_dict.get(date + "day", list()) + [j]
        else:
            weather_dict[date + "night"] = weather_dict.get(date + "night", list()) + [j]

    humidity_dict = {k: f"{max(i)}%" for k, i in humidity_dict.items()}
    weather_dict = {k: f"{round(mean(i), 2)}° C" for k, i in weather_dict.items()}
    headers = ["Date", "Day Tempature", "Night Tempature", "Max Humidity"]
    data = []
    ix = 0
    for i, j, k in zip(humidity_dict.keys(), range(0, len(weather_dict.values()), 2), humidity_dict.values()):
        data.append(list())
        data[ix].append(i)
        if j == 0:
            data[ix].append(list(weather_dict.values())[j])
            data[ix].append(list(weather_dict.values())[j + 1])
        else:
            data[ix].append(list(weather_dict.values())[j + 1])
            data[ix].append(list(weather_dict.values())[j])
        data[ix].append(k)
        ix += 1
    return render_template("result.html", country=country, city=city, headers=headers, data=data)

if __name__ == "__main__":
    app.run(debug=True)
