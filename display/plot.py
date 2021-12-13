import os
import pickle
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import *


def plot_residual():
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


def plot_sentiment_pie():
    """Read in the twitter csv and draw a pie chart showing
    the proportion of positive and negative tweets. """
    cwd = os.path.dirname(os.path.abspath(__file__))
    twitter_dir = os.path.join(cwd, "data/tweet_with_sentiment_local.csv")
    twitter_df = pd.read_csv(twitter_dir, index_col=0)
    positive_counts = sum(twitter_df["Polarity"] > 0)
    negative_counts = sum(twitter_df["Polarity"] < 0)
    colors = ['rgb(158,202,225)', 'mediumturquoise']
    fig = go.Figure(data=[go.Pie(labels=['Positive', 'Negative'],
                                 values=[positive_counts, negative_counts])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    graph = fig.to_html(full_html=False)
    return graph
