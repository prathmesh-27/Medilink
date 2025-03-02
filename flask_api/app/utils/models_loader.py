import pickle
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

mlb_disease_path  = 'flask_api\\app\\models\\mlb_disease.pkl'
mlb_diet_path = 'flask_api\\app\\models\\mlb_diet.pkl'
mlb_nutrient_path = 'flask_api\\app\\models\\mlb_nutrient.pkl'
multi_output_model_path = 'flask_api\\app\\models\\multi_output_model.pkl'


def load_models():
    """Loads all models and binarizers."""
    with open(mlb_disease_path, "rb") as file:
        mlb_disease = pickle.load(file)

    with open(mlb_diet_path, "rb") as file:
        mlb_diet = pickle.load(file)

    with open(mlb_nutrient_path, "rb") as file:
        mlb_nutrient = pickle.load(file)

    with open(multi_output_model_path, "rb") as file:
        multi_output_model = pickle.load(file)

    return mlb_disease, mlb_diet, mlb_nutrient, multi_output_model
