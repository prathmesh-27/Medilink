from datetime import date
from django import template

register = template.Library()

@register.filter
def calculate_age(dob):
    if not dob:
        return "N/A" 
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))



def calculate_bmi(height,weight):
    """Returns the BMI value rounded to 2 decimal places."""
    if height and weight:  # Ensure values exist
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
    return None  # Return None if data is missing

def get_bmi_category(bmi):
    """Returns the BMI category based on WHO standards."""
    if bmi is None:
        return "No data"
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"
    
def calculate_bmr(height,weight,dob,gender):
    """Calculates Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation."""
    if height and weight and dob and gender:
        age = calculate_age(dob)
        if not age:
            return None

        if gender.lower() == "male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:  # Female
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        return round(bmr, 2)
    return None    
    
def calculate_tdee(bmr,activity_level):
    """Calculates Total Daily Energy Expenditure (TDEE)"""
    ACTIVITY_LEVELS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "very_active": 1.725,
    "super_active": 1.9,
    }     
    activity_factor = ACTIVITY_LEVELS.get(activity_level, 1.2) 
    return round(bmr * activity_factor, 2) if bmr else None

def calories_needed(tdee,goal="maintain"):
    """Calculates Calories Needed based on Goal"""
    if not tdee:
        return None
    if goal == "lose":
        return round(tdee - 500, 2)  # 500 kcal deficit per day
    elif goal == "gain":
        return round(tdee + 500, 2)  # 500 kcal surplus per day
    return tdee  # Maintain weight