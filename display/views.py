from django.shortcuts import render
import os
from . import getweather, getprediction, gettwitter, plot, utils
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    if request.method == 'POST' and 'twitter_update_button' in request.POST:
        gettwitter.update_tweets(int(request.POST["twitter_time_interval"]))
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST' and 'weather_update_button' in request.POST:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST' and 'prediction_update_button' in request.POST:
        getprediction.get_prediction()
        return HttpResponseRedirect(reverse('dashboard'))

    temp_and_wind_dic = getweather.get_weather_ohe()
    prediction_dict = utils.load_prediction_dict()
    prediction_graph = plot.plot_residual()
    twitter_df = utils.load_twitter_df()
    sentiment_pie_chart = plot.plot_sentiment_pie()

    context = {"weather_cols": temp_and_wind_dic.keys(),
               "weather_stats": temp_and_wind_dic.values(),
               "twitter_cols": twitter_df.columns,
               "twitter_rows": twitter_df.to_dict("records"),
               "prediction_cols": prediction_dict.keys(),
               "prediction_values": prediction_dict.values(),
               "prediction_graph": prediction_graph,
               "sentiment_pie": sentiment_pie_chart}
    return render(request, 'display/dashboard.html', context)
