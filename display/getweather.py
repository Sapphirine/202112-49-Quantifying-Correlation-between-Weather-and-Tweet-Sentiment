from pyowm.owm import OWM
import pickle
import os

APIKEY = 'c793c1dd5e4c10cfa3d5a520cd1161bc'


def get_realtime_weather():
    """Get realtime weather as dict. """
    owm = OWM(APIKEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('New York').weather
    temp_dict_celsius = weather.temperature('celsius')
    wind_dict_in_meters_per_sec = weather.wind()
    temp_and_wind = {**temp_dict_celsius, **wind_dict_in_meters_per_sec}
    return temp_and_wind


def get_weather_ohe():
    cwd = os.path.dirname(os.path.abspath(__file__))
    owm = OWM(APIKEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('New York').weather
    celsius_temp = weather.temperature('celsius')
    weather_dict = {
        "Temperature": celsius_temp['temp'],
        "Status_Clear": 0,
        "Status_Clouds": 0,
        "Status_Haze": 0,
        "Status_Mist": 0,
        "Status_Rain": 0,
        "Status_Snow": 0
    }
    if weather.status == "Clear":
        weather_dict["Status_Clear"] += 1
    elif weather.status == "Clouds":
        weather_dict["Status_Clouds"] += 1
    elif weather.status == "Rain":
        weather_dict["Status_Rain"] += 1
    elif weather.status == "Haze":
        weather_dict["Status_Haze"] += 1
    elif weather.status == "Mist":
        weather_dict["Status_Mist"] += 1
    elif weather.status == "Snow":
        weather_dict["Status_Snow"] += 1

    weather_dict_dir = os.path.join(cwd, "data/weather_dict.pkl")
    with open(weather_dict_dir, "wb") as f:
        pickle.dump(weather_dict, f)

    return weather_dict

if __name__ == "__main__":
    get_weather_ohe()
