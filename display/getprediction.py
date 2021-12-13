import os
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *


def get_prediction():
    cwd = os.path.dirname(os.path.abspath(__file__))
    weather_dict_dir = os.path.join(cwd, "data/weather_dict.pkl")
    with open(weather_dict_dir, "rb") as f:
        weather_dict = pickle.load(f)
    weather_df = pd.DataFrame(weather_dict, index=[0])

    models = [
        "LinearRegression",
        "RidgeRegression1",
        "RidgeRegression2",
        "RidgeRegression3",
        "SVR"
    ]
    res = []
    for model in models:
        model_dir = os.path.join(cwd, f"updatedmodels/{model}.sav")
        with open(model_dir, "rb") as f:
            reg = pickle.load(f)
        prediction = reg.predict(weather_df).flatten()
        res.append(prediction[0])

    res_dict = {models[i]: res[i] for i in range(len(models))}

    tweet_dir = os.path.join(cwd, "data/tweet_with_sentiment_local.csv")
    tweet_with_sentiment_df = pd.read_csv(tweet_dir, index_col=0)
    pos_count = sum(tweet_with_sentiment_df["Polarity"] > 0)
    neg_count = sum(tweet_with_sentiment_df["Polarity"] < 0)

    res_dict["Current Sentiment"] = pos_count / (pos_count + neg_count)

    prediction_dir = os.path.join(cwd, "data/prediction_dict.pkl")
    with open(prediction_dir, 'wb') as f:
        pickle.dump(res_dict, f)
    return res_dict


def plot_difference():
    """Read in the prediction dictionary and draw a plotly express graph. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    prediction_dir = os.path.join(cwd, "data/prediction_dict.pkl")
    with open(prediction_dir, 'rb') as f:
        prediction_dict = pickle.load(f)

    prediction_diff = {model: prediction_dict[model] - prediction_dict["Current Sentiment"]
                       for model in prediction_dict.keys() if model != "Current Sentiment"}
    prediction_diff_df = (pd.DataFrame.from_dict(prediction_diff, orient="index")
                          .reset_index().rename(columns={"index": "Models", 0: "Residual"}))
    x = prediction_diff_df["Models"]
    y = prediction_diff_df["Residual"]
    layout = Layout(
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto'
    )], layout=layout)
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    graph = fig.to_html(full_html=False)
    return graph
