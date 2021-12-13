import os
import pickle
import pandas as pd


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

