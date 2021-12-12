from pyowm.owm import OWM


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


if __name__ == '__main__':
    get_realtime_weather()


