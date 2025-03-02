from flask import Blueprint, render_template, request,jsonify
from .utils.utility import *


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Hello")
    return render_template('index.html', recommendations=None)

@main.route('/process-data', methods=['POST'])
def process_data():
    data = request.json  # Get JSON data from Django
    processed_data = {"message": "Processed successfully", "input": data}
    return jsonify(processed_data)


nutrients = ['calcium', 'carbohydrates', 'chloride', 'fiber', 'iron', 'magnesium', 'manganese', 'phosphorus', 'potassium', 'protien', 'selenium', 'sodium', 'vitamin_a', 'vitamin_c', 'vitamin_e']
health_conditions = ['anemia', 'cancer', 'diabeties', 'eye_disease', 'goitre', 'heart_disease', 'hypertension', 'kidney_disease', 'obesity', 'pregnancy', 'rickets', 'scurvy']

@main.route('/diet', methods=['GET', 'POST'])
def diet():
    if request.method == 'POST':
        selected_nutrients = request.form.getlist('nutrients')
        selected_conditions = request.form.getlist('health_conditions')
        selected_gender = request.form.get('gender')
        selected_type = request.form.get('foodtype')
        
        # Encode inputs and predict
        X = encode_inputs(selected_conditions, selected_nutrients)
        predicted_diet_labels = predict_diet(X)  
        
        # Prepare data
        data = {
            "diet_labels": predicted_diet_labels,
            "gender": selected_gender,
            "food_type": selected_type,
            "flattened_data": selected_nutrients + selected_conditions + list(predicted_diet_labels[0])
        }   
        
        results = predict_foods(data['flattened_data'],selected_type)
        df_html = results.to_html(classes='table table-striped')
        
        if request.is_json:  # If Django is expecting HTML, we can return raw HTML
            return jsonify(df_html)
        
        return render_template('result.html', data = data, df_html=df_html)
    
    return render_template('diet.html', nutrients=nutrients, health_conditions=health_conditions)



excercise = ['sedentary','lightly_active','moderately_active','very_active','super_active']

@main.route('/calorie', methods=['GET', 'POST'])
def calorie_dashboard():
    if request.method == 'POST':
        gender = request.form.get('gender')
        age = int(request.form.get('age'))
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        activity = request.form.get('activity_type')
        BMR =  calculate_bmr(weight,height,age,gender)
        BMI = calculate_bmi(weight_kg=weight,height_cm=height)
        
        data = {
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "exercise": activity,
            "BMI": BMI ,
            "BMI_category":bmi_category(BMI),
            "BMR": BMR,
            "calories":calorie_calculator(BMR,activity),
             
        }
        
        return render_template('cresult.html',data=data)
        
  

        
    return render_template('calories.html', excercise = excercise)   