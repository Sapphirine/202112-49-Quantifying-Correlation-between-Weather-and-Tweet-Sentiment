import pandas as pd
import plotly.graph_objects as go
from . import utils
from plotly.subplots import make_subplots


def generate_plots():
    """Generate the residual graph and the pie chart. """
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{"type": "xy"}, {"type": "xy"}, {"type": "domain"}]],
                        subplot_titles=("RMSE with Historical Data", "Residual", "Proportion of Sentiment"))
    prediction_dict = utils.load_prediction_dict()
    prediction_diff = {model: prediction_dict[model] - prediction_dict["Current Sentiment"]
                       for model in prediction_dict.keys() if model != "Current Sentiment"}
    prediction_diff_df = (pd.DataFrame.from_dict(prediction_diff, orient="index")
                          .reset_index().rename(columns={"index": "Models", 0: "Residual"}))
    x = prediction_diff_df["Models"]
    y = prediction_diff_df["Residual"]

    fig.add_trace(go.Bar(x=x, y=[0.07111215273319181,
                                 0.07111232540379143,
                                 0.06779278771721373,
                                 0.06233706995564963,
                                 0.0714032585657523,
                                 0.03276174377125942],
                         textposition="auto",
                         marker=dict(color="rgb(158,202,225)",
                                     line_color="rgb(8,48,107)",
                                     line_width=1.5),
                         opacity=0.8, name="RMSE"),
                  row=1, col=1)

    fig.add_trace(go.Bar(
        x=x, y=y,
        textposition='auto',
        marker=dict(color='lightsalmon',
                    line_color="rgb(8,48,107)",
                    line_width=1.5),
        opacity=0.8,
        name="Residual"
    ), row=1, col=2)

    twitter_df = utils.load_twitter_df()
    positive_counts = sum(twitter_df["Polarity"] > 0)
    negative_counts = sum(twitter_df["Polarity"] < 0)
    colors = ['gold', 'mediumturquoise']
    fig.add_trace(go.Pie(labels=['Positive', 'Negative'],
                         values=[positive_counts, negative_counts],
                         marker=dict(colors=colors, line=dict(color='#000000', width=2)),
                         opacity=0.8,
                         name="Pie"), row=1, col=3)
    # fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    graph = fig.to_html(full_html=False)
    return graph
