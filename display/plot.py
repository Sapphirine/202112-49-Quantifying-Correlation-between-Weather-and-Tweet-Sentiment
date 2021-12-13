import pandas as pd
import plotly.graph_objects as go
from . import utils
from plotly.subplots import make_subplots


def generate_plots():
    """Generate the residual graph and the pie chart. """
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}]])
    prediction_dict = utils.load_prediction_dict()
    prediction_diff = {model: prediction_dict[model] - prediction_dict["Current Sentiment"]
                       for model in prediction_dict.keys() if model != "Current Sentiment"}
    prediction_diff_df = (pd.DataFrame.from_dict(prediction_diff, orient="index")
                          .reset_index().rename(columns={"index": "Models", 0: "Residual"}))
    x = prediction_diff_df["Models"]
    y = prediction_diff_df["Residual"]

    fig.add_trace(go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
        marker=dict(color="rgb(158,202,225)",
                    line_color="rgb(8,48,107)",
                    line_width=1.5),
        opacity=0.6,
        name="Residual"
    ), row=1, col=1)

    twitter_df = utils.load_twitter_df()
    positive_counts = sum(twitter_df["Polarity"] > 0)
    negative_counts = sum(twitter_df["Polarity"] < 0)
    colors = ['gold', 'mediumturquoise']
    fig.add_trace(go.Pie(labels=['Positive', 'Negative'],
                         values=[positive_counts, negative_counts],
                         marker=dict(colors=colors, line=dict(color='#000000', width=2))), row=1, col=2)
    # fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    graph = fig.to_html(full_html=False)
    return graph
