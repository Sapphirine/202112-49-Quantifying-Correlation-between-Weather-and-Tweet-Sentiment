from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
import tweepy
from . import getweather


# Create your views here.
def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    work = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(work, 'weather_storage.csv')
    df = pd.read_csv(path)
    temp_and_wind = getweather.get_realtime_weather()
    context = {"columns": df.columns,
               'rows': df.to_dict('records'),
               "weather_cols": temp_and_wind.keys(),
               "weather_stats": temp_and_wind.values()}
    return render(request, 'display/dashboard.html', context)
