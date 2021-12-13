from django.shortcuts import render
import pandas as pd
import os
from . import getweather, getprediction
from django.http import HttpResponseRedirect
from django.urls import reverse
import pickle


def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    workdir = os.path.dirname(os.path.abspath(__file__))
    if request.method == 'POST' and 'twitter_update_button' in request.POST:
        twitter_time_interval = int(request.POST["twitter_time_interval"])
        from . import gettwitter
        gettwitter.update_tweets(twitter_time_interval)
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST' and 'weather_update_button' in request.POST:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST' and 'prediction_update_button' in request.POST:
        getprediction.get_prediction()
        return HttpResponseRedirect(reverse('dashboard'))

    temp_and_wind_dic = getweather.get_weather_ohe()

    with open(os.path.join(workdir, "data/prediction_dict.pkl"), "rb") as f:
        prediction_dict = pickle.load(f)

    graph = getprediction.plot_difference()
    twitter_df = (pd.read_csv(os.path.join(workdir, "data/tweet_with_sentiment_local.csv"),
                              index_col=0))
    context = {"weather_cols": temp_and_wind_dic.keys(),
               "weather_stats": temp_and_wind_dic.values(),
               "twitter_cols": twitter_df.columns,
               "twitter_rows": twitter_df.to_dict("records"),
               "prediction_cols": prediction_dict.keys(),
               "prediction_values": prediction_dict.values(),
               "graph": graph}
    return render(request, 'display/dashboard.html', context)
