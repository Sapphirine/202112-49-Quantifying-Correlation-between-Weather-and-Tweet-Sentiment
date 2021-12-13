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
        "LinearRegression.sav",
        "RidgeRegression1.sav",
        "RidgeRegression2.sav",
        "RidgeRegression3.sav",
        "SVR.sav"
    ]
    res = []
    for model in models:
        model_dir = os.path.join(cwd, f"updatedmodels/{model}")
        with open(model_dir, "rb") as f:
            reg = pickle.load(f)
        prediction = reg.predict(weather_df).flatten()
        res.append(prediction[0])

    res_dict = {models[i]: res[i] for i in range(len(models))}
    prediction_dir = os.path.join(cwd, "data/prediction_dict.pkl")
    with open(prediction_dir, 'wb') as f:
        pickle.dump(res_dict, f)
    return res_dict
