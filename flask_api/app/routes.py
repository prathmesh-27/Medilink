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

conversation_data = {}

@main.route("/chat", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()
    user_id = request.json.get("user_id", "default_user")

    if user_id not in conversation_data:
        conversation_data[user_id] = {}
        
    convo = conversation_data[user_id]

    if "appointment" in user_message:
        convo.clear()
        return jsonify({"response": "Sure! Please enter your name with last name.(Name is 'Your Name')"})

    elif "name is" in user_message:
        full_name = user_message.replace("name is", "").strip().title()
    
        # Split the full name into parts (first and last name)
        name_parts = full_name.split()
    
        # Assuming the user enters both first and last names
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]
        
            # Store the names in the conversation dictionary
            convo["first_name"] = first_name
            convo["last_name"] = last_name
        
            print(f"First Name: {first_name}, Last Name: {last_name}")
            return jsonify({"response": f"Got it {first_name}! Please provide me with your dob.(dob is 'yyyy-mm-dd')"})
        else:
            return jsonify({"response": "Please provide both your first and last name."})

    
    elif "dob is" in user_message:
        dob = user_message.replace("dob is", "").strip()
        convo["dob"] = dob
        return jsonify({"response": "Please provide your gender. (gender is Male/Female)"})

    elif "gender is" in user_message:
        gender = user_message.replace("gender is", "").strip().capitalize()
    
        if gender in ["Male", "Female"]:
            convo["gender"] = gender
            return jsonify({"response": "Thanks! Now, please provide your 10-digit mobile number.(mobile number is XXXXXXXXXX) first digit should be 7/8/9"})
        else:
            return jsonify({"response": "Invalid input. Please enter your gender as 'Male' or 'Female'."})

    elif "mobile number is" in user_message:
        mobile = user_message.replace("mobile number is", "").strip()
    
        if mobile.isdigit() and len(mobile) == 10:
            convo["mobile"] = mobile
            departments = get_all_departments()
            return jsonify({"response": f"Thanks, {convo["first_name"]}! What specialization do you need? ({', '.join(dept.title() for dept in departments)})"})    
    
        else:
            return jsonify({"response": "Invalid mobile number. Please enter a valid 10-digit number."})

        
    elif any(dept in user_message for dept in get_all_departments()):
        selected_specialty = next((d for d in get_all_departments() if d in user_message), None)
        print(selected_specialty)
        convo["specialty"] = selected_specialty

        doctors = get_doctors_by_specialty(selected_specialty)
        doctor_names = [f"Dr. {doctor['name']}" for doctor in doctors]

        return jsonify({
            "response": f"We have {', '.join(doctor_names)} available. Please give doctor name as (Dr. Name)."
        })

    elif "dr." in user_message:
        selected_doc = user_message.replace("dr.", "").strip().title()
        convo["doctor"] = selected_doc

        doctor_obj = get_doctor_by_name(selected_doc)
        if not doctor_obj:
            return jsonify({"response": "Doctor not found. Please try again."})
        
        doctor_id = int(doctor_obj[0]["id"]) 
        
        availabilities = get_available_dates(doctor_id)
        dates = availabilities["available_dates"]
        convo['available_dates'] = dates
        convo["doctor_id"] = doctor_id
        
        if not dates:
            return jsonify({"response": f"Sorry! Dr. {selected_doc} has no available schedule at the moment. Please try another doctor or check back later."})

        formatted_dates = [f"{get_day_of_week(date)} ({date})" for date in dates]
        return jsonify({"response": f"Dr. {selected_doc} is available on:<br>{'<br>'.join(formatted_dates)}<br>Please choose a date. (YYYY-MM-DD)"})

    elif is_valid_date_format(user_message):
        doctor = get_doctor_by_id(convo["doctor_id"])
        appointment_date = user_message
        convo['appointment_date'] = appointment_date
        return jsonify({
            "response": f"""Please confirm Your details:<br> 
             Name: {convo['first_name']+" "+convo["last_name"] },<br> 
             Date of Birth: {convo['dob']},<br>
             Gender: {convo['gender']},<br>
             Mobile Number: {convo['mobile']},<br>
             Your appointment with Dr. {convo['doctor']} on {appointment_date} ({get_day_of_week(appointment_date)}).<br>
             For timings you Can Call XXX-XXXXXX<br>
             Please reply 'confirm' or 'cancel'."""
        })

    elif user_message.lower() == "confirm":
    # Send confirmation to Django app
        appointment_day = get_day_of_week(convo['appointment_date'])
        data = {
            "first_name": convo['first_name'],
            "last_name": convo['last_name'],
            "dob": convo['dob'],
            "gender": convo['gender'],
            "mobile": convo['mobile'],
            "doctor_id": convo["doctor_id"],
            "appointment_date": convo['appointment_date'],
            }

        try:
            # Send the data to Django (you should set up a Django API endpoint to receive this data)
            response = requests.post("http://localhost:8000/api/schedule_appointment/", json=data)

            if response.status_code == 200:
            # Check if the response contains more detailed information (e.g., email, password, etc.)
                response_data = response.json()
        
                if response_data.get("status") == "success":
                # Handle success
                    conversation_data.pop(user_id, None)
                    return jsonify({
                        "response": f"Thanks, {response_data.get('first_name')}!<br> Your appointment with Dr. {response_data.get('first_name')} on {response_data.get('appointment_date')} ({get_day_of_week(response_data.get('appointment_date'))}).<br>Your Appointment is {response_data.get('appointment_id')} You can now log in with your Username: {response_data.get('username')} and password: {response_data.get('password')}."
                    })
                else:
                    return jsonify({
                        "response": "Sorry, there was an issue confirming your appointment. Please try again later."
                        })
                    
            else:
                return jsonify({
                        "response": f"Error {response.status_code}: There was an issue with the server. Please try again later."
                        })  
                
        except Exception as e:
                return jsonify({"response": f"An error occurred: {str(e)}"})

    elif "cancel" in user_message:
        conversation_data.pop(user_id, None)
        return jsonify({"response": "Appointment booking canceled."})


    return jsonify({
        "response": "I'm here to assist with doctor appointments. Say 'book an appointment' to start."
    })

@main.route('/reset', methods=['POST'])
def reset_chat():
    conversation_data.clear()  # Clear session or chat history
    return jsonify({"message": "Conversation reset successfully."})
