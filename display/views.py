from django.shortcuts import render
from . import getweather, getprediction, gettwitter, plot, utils
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    context = {}
    return render(request, 'display/index.html', context)


def dashboard(request):
    if request.method == 'POST' and 'update_button' in request.POST:
        gettwitter.update_tweets(int(request.POST["twitter_time_interval"]))
        getprediction.get_prediction()
        return HttpResponseRedirect(reverse('dashboard'))

    temp_and_wind_dic = getweather.get_weather_ohe()
    prediction_dict = utils.load_prediction_dict()
    twitter_df = utils.load_twitter_df()
    combined_graph = plot.generate_plots()

    context = {"weather_cols": temp_and_wind_dic.keys(),
               "weather_stats": temp_and_wind_dic.values(),
               "twitter_cols": twitter_df.columns,
               "twitter_rows": twitter_df.to_dict("records"),
               "prediction_cols": prediction_dict.keys(),
               "prediction_values": prediction_dict.values(),
               "combined_graph": combined_graph,
               "temperature": temp_and_wind_dic["Temperature"],
               "sentiment": utils.get_sentiment(twitter_df)}
    return render(request, 'display/dashboard.html', context)
