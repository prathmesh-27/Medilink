from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.http import HttpResponseRedirect,JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout,authenticate,login
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import now


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    loginform = forms.LoginForm()
    signupform = forms.AdminSigupForm()
    return render(request,'hospital/index.html',{'loginform':loginform,'signupform':signupform})

def aboutus_view(request):
    return render(request,'hospital/other/aboutus.html',{'title': 'About Us'})

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            messages.success(request, 'Your message has been successfully sent! We will get back to you soon.')
            return render(request, 'hospital/other/contactus.html')
        
    return render(request, 'hospital/other/contactus.html', {'form':sub})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})

def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient/patient_view_doctor.html',{'patient':patient,'doctors':doctors})

def load_form(request):
    form_type = request.GET.get('form_type')
    loginform = forms.LoginForm()
    
    if form_type == "admin":
        signupform = forms.AdminSigupForm()
        template = "hospital/dummy/admin_form.html"
        
    elif form_type == "doctor":
        doctorForm = forms.DoctorForm()
        userForm = forms.DoctorUserForm()
        signupform = {"doctor":doctorForm,"user":userForm}
        print(signupform)
        template = "hospital/dummy/doctor_form.html"

    elif form_type == "patient":
        patientForm = forms.PatientForm()
        userForm = forms.PatientUserForm()
        signupform = {"patient":patientForm,"user":userForm}
        template = "hospital/dummy/patient_form.html"

    else:
        return render(request, "hospital/error.html", {"message": "Invalid form type"})
    
    # print(signupform)
    return render(request, template, {"loginform": loginform ,"signupform": signupform})


def get_departments(request):
    # Get the unique departments and convert each to lowercase
    departments = [dept[0].lower() for dept in models.Doctor._meta.get_field('department').choices]
    return JsonResponse(departments, safe=False)


def get_doctors_by_specialty(request, specialty):
    doctors = models.Doctor.objects.filter(department__iexact=specialty, status=True)
    data = [
        {
            "id": doctor.get_id,                # Custom ID property from model
            "name": doctor.get_name,            # Full name (first + last)    
        }
        for doctor in doctors
    ]
    return JsonResponse(data, safe=False)

def get_doctor_by_name(request, selected_doc):
    first_name,last_name = selected_doc.split()
    # Query for doctor based on name (using case-insensitive search)
    doctors =  models.Doctor.objects.filter(user__first_name__icontains=first_name) & models.Doctor.objects.filter(user__last_name__icontains=last_name)
    # If no doctor is found
    if not doctors.exists():
        return JsonResponse({"response": "No doctor found with that name."}, status=404)
    # Format data to return
    data = [
        {
            "id":doctor.id,
            "doctor_user_id": doctor.get_id,
            "name": doctor.get_name,
        }
        for doctor in doctors
    ]
    
    return JsonResponse(data, safe=False)


def get_available_dates(request,doctor_id):
    today = now().date()  # Get today's date
    
    # Step 1: Get all the availability dates for the doctor, greater than today
    available_dates = models.DoctorAvailability.objects.filter(
        doctor_id=doctor_id,  # Match the doctor user ID
        date_available__gt=today  # Only dates greater than today
    ).values_list('date_available', flat=True).distinct()

    doctor = models.Doctor.objects.get(id=doctor_id)
    # Step 2: Get all appointment dates for the doctor (using doctor's user ID)
    booked_dates = models.Appointment.objects.filter(
        doctorId=doctor.user.id,
        appointmentDate__gt=today,  # Only dates greater than today
        status=True
    ).values_list('appointmentDate', flat=True)

    # Step 3: Filter out the dates that are already booked in the Appointment model
    free_dates = [date for date in available_dates if date not in booked_dates]

    return JsonResponse({"available_dates": free_dates}, safe=False)


def get_available_dates_by_user(request, user_id):
    try:
        doctor = models.Doctor.objects.get(user_id=user_id)
    except models.Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)

    today = now().date()

    available_dates = models.DoctorAvailability.objects.filter(
        doctor=doctor,
        date_available__gt=today
    ).values_list('date_available', flat=True).distinct()

    booked_dates = models.Appointment.objects.filter(
        doctorId=doctor.user.id,
        appointmentDate__gt=today,
        status=True
    ).values_list('appointmentDate', flat=True)

    free_dates = [str(date) for date in available_dates if date not in booked_dates]

    return JsonResponse({"available_dates": free_dates})



def generate_username(first_name, last_name):
    # Simple logic to generate username based on first and last name
    username = f"{first_name.lower()}.{last_name.lower()}"
    # Ensure the username is unique
    count = 1
    while models.User.objects.filter(username=username).exists():
        username = f"{first_name.lower()}.{last_name.lower()}{count}"
        count += 1
    return username

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.contrib.auth.models import Group

@csrf_exempt
def schedule_appointment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        print(data)
        
        # Extract data from request
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        dob = data.get("dob")
        gender = data.get("gender")
        mobile = data.get("mobile")
        doctor_id = data.get("doctor_id")
        appointment_date = data.get("appointment_date")

        
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(100,999)}"
        
        password = "1234"

        # Create user
        user = models.User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name)
        
        
        
        patient_group, created = Group.objects.get_or_create(name='PATIENT')
        patient_group.user_set.add(user)
        
        doctor = models.Doctor.objects.get(id=doctor_id)  # Get the doctor instance by doctor_id
        doctor_name = doctor.get_name
        
       # Create patient
        patient = models.Patient.objects.create(
            user=user,
            mobile=mobile,
            gender=gender,
            dob=dob,
            address="Not Provided",
            symptoms="Not Provided",
            assignedDoctorId=doctor.user.id,
            is_emergency=True,
            is_discharged=False,
            status=True
        )
        
                # Create the Appointment record with the doctor's user id
        appointment = models.Appointment.objects.create(
            patientId=patient.user.id,
            doctorId=doctor.user.id,  # Store the doctor_user_id in the appointment
            patientName=f"{first_name} {last_name}",
            doctorName= doctor.get_name,  
            appointmentDate = appointment_date,
            appointment_day=None,  # Set to None or a default value if not provided
            description='Not Specified',  # Set to None if no description is provided
            status=True  
        )
        
        
        # Return confirmation with user details
        return JsonResponse({
            "status": "success",
            "message": "Appointment confirmed successfully!",
            "appointment_id": appointment.id,
            "appointment_date":appointment_date,
            "first_name":first_name,
            "doctor_name":doctor.get_name,
            "username": username,
            "password": password
        })
    return JsonResponse({"status": "error", "message": "Invalid request method."})