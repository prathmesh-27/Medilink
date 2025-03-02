from .models_loader import load_models
import pandas as pd
from app.diet_recommender import Recommender

mlb_disease, mlb_diet, mlb_nutrient, multi_output_model = load_models()

def encode_inputs(selected_conditions, selected_nutrients):
    x_disease = mlb_disease.transform([selected_conditions])
    x_nutrient = mlb_nutrient.transform([selected_nutrients])
    encoded_df = pd.concat(
        [pd.DataFrame(x_disease, columns=mlb_disease.classes_),
         pd.DataFrame(x_nutrient, columns=mlb_nutrient.classes_)],
        axis=1
    )
    return encoded_df

def predict_diet(encoded_features):
    predicted = multi_output_model.predict(encoded_features)
    return mlb_diet.inverse_transform(predicted)

def predict_foods(features, type):
    recommend = Recommender()  # Assuming Recommender is properly defined
    data = recommend.get_features()  # Get the data (pandas DataFrame)
    total_features = data.columns  # All feature names from the data

    # Initialize the dictionary with features set to 0
    d = {feature: 0 for feature in total_features}

    # Set selected features to 1
    for feature in features:
        if feature in d:
            d[feature] = 1

    # Convert the dictionary to a list of values for the input
    final_input = list(d.values())

    # Assuming k_neighbor returns a DataFrame
    results = recommend.k_neighbor([final_input])  # Pass 2D array [final_input]

    # Make sure results is a pandas DataFrame and filter by 'Veg_Non'
    if isinstance(results, pd.DataFrame):
        filtered_results = results[results['Veg_Non'] == type]
    else:
        filtered_results = []

    # Clean up unnecessary variables (optional in this case)
    del d, data, recommend, total_features

    return filtered_results

def calorie_calculator(BMR , activity_level):
    
    # Activity factor based on activity level
    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "super_active": 1.9
    }
    
    TDEE = BMR * activity_factors.get(activity_level.lower(), 1.2)
    
    return round(TDEE,2)

def calculate_bmi(weight_kg, height_cm):
    # Calculate BMI
    bmi = weight_kg / ((height_cm/100) ** 2)
    return round(bmi,2)

def bmi_category(bmi):
    # Determine BMI category
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender.lower() == "male":
        # Mifflin-St Jeor Equation for Men
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        # Mifflin-St Jeor Equation for Women
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr,2)    
    

    