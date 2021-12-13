import pandas as pd
import os
import pickle


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
