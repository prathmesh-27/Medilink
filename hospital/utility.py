from datetime import date
from django import template
from hospital import models
from django.db.models import Count
from django.utils.timezone import now, timedelta
import json

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

def get_age_groups():
    """Getting the age groups of patients"""
    today = date.today()
    age_groups = {
        '0-18': 0,   # 0-18
        '19-35': 0,  # 19-35
        '36-50': 0,  # 36-50
        '51+': 0     # 51+
    }

    patients = models.Patient.objects.filter(dob__isnull=False)

    for patient in patients:
        age = today.year - patient.dob.year - ((today.month, today.day) < (patient.dob.month, patient.dob.day))
        
        if age <= 18:
            age_groups['0-18'] += 1
        elif 19 <= age <= 35:
            age_groups['19-35'] += 1
        elif 36 <= age <= 50:
            age_groups['36-50'] += 1
        else:
            age_groups['51+'] += 1
            
    age_groups = json.dumps({
        'labels': list(age_groups.keys()),
        'data': list(age_groups.values())
    })        
    return age_groups

def get_admissions_by_month():
    # Get current year
    current_year = now().year  

    # Query database to count admissions per month
    admissions = (
        models.Patient.objects.filter(admitDate__year=current_year)
        .values('admitDate__month')
        .annotate(count=Count('id'))
        .order_by('admitDate__month')
    )

    # Map numeric months to names
    month_map = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # Prepare labels and data for Chart.js
    labels = []
    data = []

    for entry in admissions:
        month_num = entry['admitDate__month']
        labels.append(month_map[month_num])  # Convert month number to name
        data.append(entry['count']) # Add patient count for that month

    line_graph = json.dumps({
        'labels': labels,
        'data': data
    })

    return line_graph

def get_doctors_by_departments():
    # Count doctors in each department
    department_counts = (
        models.Doctor.objects.values('department')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Convert QuerySet to JSON-friendly format
    chart_data = {
        'labels': [entry['department'] for entry in department_counts],
        'data': [entry['count'] for entry in department_counts]
    }

    return json.dumps(chart_data)


def get_patients_division_data():
    # Get all department names from choices
    departments = [dept[0] for dept in models.Doctor._meta.get_field('department').choices]

    # Initialize patient count storage for male and female
    male_counts = {dept: 0 for dept in departments}
    female_counts = {dept: 0 for dept in departments}

    # Get all doctors and map their ID to their department
    doctor_depts = {doc.user_id: doc.department for doc in models.Doctor.objects.all()}

    # Query patients grouped by assignedDoctorId and gender
    patient_counts = (
        models.Patient.objects.exclude(assignedDoctorId=None)  # Ignore unassigned patients
        .values('assignedDoctorId', 'gender')
        .annotate(count=Count('id'))
    )
    print(patient_counts)
    # Fill the count data
    for entry in patient_counts:
        doctor_id = entry['assignedDoctorId']
        gender = entry['gender']
        count = entry['count']

        # Ensure doctor exists in mapping
        if doctor_id in doctor_depts:
            department = doctor_depts[doctor_id]
            if gender == "Male":
                male_counts[department] += count
            elif gender == "Female":
                female_counts[department] += count

    # Convert the data to JSON format
    patients_by_division = {
        'labels': departments,
        'male_data': list(male_counts.values()),
        'female_data': list(female_counts.values())
    }

    return json.dumps(patients_by_division)

def get_appointment_rate():
    # Get total number of appointments in the last 30 days
    today = now().date()
    past_30_days = today - timedelta(days=30)

    total_appointments = models.Appointment.objects.filter(appointmentDate__gte=past_30_days).count()

    # Calculate the average per day
    avg_per_day = total_appointments / 30 if total_appointments > 0 else 0
    return round(avg_per_day, 2)