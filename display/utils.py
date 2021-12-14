import pandas as pd
import os
import pickle
import numpy as np


def load_twitter_df():
    """Load the twitter csv as a dataframe. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    return (pd.read_csv(os.path.join(cwd, "data/tweet_with_sentiment_local.csv"),
                        index_col=0))


def load_prediction_dict():
    """Load the prediction_dict.pkl as a dict. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cwd, "data/prediction_dict.pkl"), "rb") as f:
        prediction_dict = pickle.load(f)
    return prediction_dict


def save_weather_dict(weather_dict):
    """Save the weather status dict as pkl. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    weather_dict_dir = os.path.join(cwd, "data/weather_dict.pkl")
    with open(weather_dict_dir, "wb") as f:
        pickle.dump(weather_dict, f)


def save_prediction_dict(prediction_dict):
    cwd = os.path.dirname(os.path.abspath(__file__))
    prediction_dir = os.path.join(cwd, "data/prediction_dict.pkl")
    with open(prediction_dir, 'wb') as f:
        pickle.dump(prediction_dict, f)


def get_sentiment(twitter_df):
    positive_counts = sum(twitter_df["Polarity"] > 0)
    negative_counts = sum(twitter_df["Polarity"] < 0)
    return positive_counts / (positive_counts + negative_counts)


def load_historic_twitter_df():
    """load the full historic twitter data, transformed with OHE. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    twitter_df = pd.read_csv(os.path.join(cwd, "data/classifier.csv"), index_col=0)
    twitter_df_ohe = pd.get_dummies(twitter_df, columns=["Status"])
    twitter_df_ohe["Polarity"] = twitter_df_ohe["Sentiment"].apply(lambda x: 1 if x == "Positive" else 0)
    return twitter_df_ohe


def get_prediction_metrics():
    cwd = os.path.dirname(os.path.abspath(__file__))
    twitter_full_df = load_historic_twitter_df()
    models = [
        "LinearRegression",
        "RidgeRegression",
        "GradientBoosting",
        "XGBoost",
        "SVR",
        "RandomForest"
    ]
    X = twitter_full_df[["Temperature", "Status_Clear", "Status_Clouds",
                         "Status_Haze", "Status_Mist", "Status_Rain", "Status_Snow"]]
    y = np.array(get_sentiment(twitter_full_df))
    for model in models:
        model_dir = os.path.join(cwd, f"updatedmodels/{model}.sav")
        with open(model_dir, "rb") as f:
            reg = pickle.load(f)
        print(f"{model}: {reg.score(X, y)}")


if __name__ == "__main__":
    get_prediction_metrics()
