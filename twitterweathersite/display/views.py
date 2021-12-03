from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from . import getweather
from . import gettwitter


def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    work = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(work, 'weather_storage.csv')
    weather_df = pd.read_csv(path)
    temp_and_wind = getweather.get_realtime_weather()
    # twitter_df = gettwitter.stream_tweets()
    twitter_path = os.path.join(work, "tweetsexample.csv")
    twitter_df = pd.read_csv(twitter_path)
    twitter_df = twitter_df.loc[:, ["created_at", "id", "text"]]
    context = {"columns": weather_df.columns,
               'rows': weather_df.to_dict('records'),
               "weather_cols": temp_and_wind.keys(),
               "weather_stats": temp_and_wind.values(),
               "twitter_cols": twitter_df.columns,
               "twitter_rows": twitter_df.to_dict("records")}
    return render(request, 'display/dashboard.html', context)
