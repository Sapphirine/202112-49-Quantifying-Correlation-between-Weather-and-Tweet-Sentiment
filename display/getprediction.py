import os
import pickle
import pandas as pd
from . import utils


def get_prediction():
    cwd = os.path.dirname(os.path.abspath(__file__))
    weather_dict_dir = os.path.join(cwd, "data/weather_dict.pkl")
    with open(weather_dict_dir, "rb") as f:
        weather_dict = pickle.load(f)
    weather_df = pd.DataFrame(weather_dict, index=[0])

    models = [
        "LinearRegression",
        "RidgeRegression",
        "GradientBoosting",
        "AdaBoost",
        "SVR",
        "RandomForest",
    ]
    res = []
    for model in models:
        model_dir = os.path.join(cwd, f"updatedmodels/{model}.sav")
        with open(model_dir, "rb") as f:
            reg = pickle.load(f)
        prediction = reg.predict(weather_df).flatten()
        res.append(prediction[0])

    res_dict = {models[i]: res[i] for i in range(len(models))}

    tweet_with_sentiment_df = utils.load_twitter_df()
    res_dict["Current Sentiment"] = utils.get_sentiment(tweet_with_sentiment_df)

    utils.save_prediction_dict(res_dict)
    return res_dict
