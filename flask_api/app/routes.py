from flask import Blueprint, render_template, request,jsonify
from .utils.utility import *


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Hello")
    return render_template('index.html', recommendations=None)



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
        
        #For Formating data
        results.columns = [col.replace("_", " ").title() for col in results.columns]
        
        df_html = results.to_html(classes='table table-striped', index=False)
        
        return jsonify({"table": df_html})


