import pickle
import numpy as np

load_neural_network = pickle.load(open("./models/load_neural_network_model.pkl", "rb"))
load_random_forsest = pickle.load(open("./models/load_random_forest_model.pkl", "rb"))
load_xgboost = pickle.load(open("./models/load_xgboost_model.pkl", "rb"))

gen_neural_network = pickle.load(open("./models/gen_neural_network_model.pkl", "rb"))
gen_random_forsest = pickle.load(open("./models/gen_random_forest_model.pkl", "rb"))
gen_xgboost = pickle.load(open("./models/gen_xgboost_model.pkl", "rb"))


models = {
    'load_neural_network': load_neural_network,
    'load_random_forsest': load_random_forsest,
    'load_xgboost': load_xgboost,
    'gen_neural_network': gen_neural_network,
    'gen_random_forsest': gen_random_forsest,
    'gen_xgboost': gen_xgboost
}


def predict_load(model_name, data):
    """
    Predict the result using the specified model and input data.

    Parameters:
    - model_name (str): The name of the model to use for prediction.
    - data (pd.DataFrame): The input data for prediction.

    Returns:
    - str: The predicted result.
    """
    # nan_columns = data.columns[data.isna().any()].tolist()
    # print(nan_columns)
    model = models[model_name]
    try:
        f_names = model.feature_names_in_
        prediction = model.predict(data[f_names])
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None
    return np.exp(prediction) - 1 


def predict_generation(model_name, data):
    """
    Predict the result using the specified model and input data.

    Parameters:
    - model_name (str): The name of the model to use for prediction.
    - data (pd.DataFrame): The input data for prediction.

    Returns:
    - str: The predicted result.
    """
    # nan_columns = data.columns[data.isna().any()].tolist()
    # print(nan_columns)
    model = models[model_name]
    missing_columns = [col for col in model.feature_names_in_ if col not in data.columns]
    print(f"Missing columns: {missing_columns}")
    try:
        f_names = model.feature_names_in_
        prediction = model.predict(data[f_names])
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None
    return np.exp(prediction) - 1 
