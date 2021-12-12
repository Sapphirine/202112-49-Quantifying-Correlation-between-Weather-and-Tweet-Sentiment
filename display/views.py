from django.shortcuts import render
import pandas as pd
import os
from . import getweather
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging


def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    workdir = os.path.dirname(os.path.abspath(__file__))
    if request.method == 'POST' and 'run_script' in request.POST:
        from . import gettwitter
        gettwitter.update_tweets()
        return HttpResponseRedirect(reverse('dashboard'))

    temp_and_wind_dic = getweather.get_realtime_weather()
    print(workdir)
    twitter_df = (pd.read_csv(os.path.join(workdir, "data/tweet_with_sentiment_local.csv"),
                              index_col=0))
    context = {"weather_cols": temp_and_wind_dic.keys(),
               "weather_stats": temp_and_wind_dic.values(),
               "twitter_cols": twitter_df.columns,
               "twitter_rows": twitter_df.to_dict("records")}
    return render(request, 'display/dashboard.html', context)
