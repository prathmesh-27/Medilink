from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib import messages
from ..utility import calculate_age,calculate_bmi,get_bmi_category,calculate_bmr,calculate_tdee,calories_needed



def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)#for profile picture of patient in sidebar
    appointments_approved =models.Appointment.objects.all().filter(patientId=request.user.id)
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None
    
    context = {'patient':patient,
               'appointments_approved':appointments_approved,
               'appointmentForm':appointmentForm,
               'role':role,}
    
    return render(request,'hospital/patient/patient_appointment.html',context)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')
            
            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-appointment')

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None
    mydict={
    'patient':patient,
    'patient_age':calculate_age(patient.dob),
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    'role':role,
    }
    return render(request,'hospital/patient/patient_dashboard.html',context=mydict)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient/patient_discharge.html',context=patientDict)


def patient_signup_view(request):
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)  # Hash password
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user

            # print(request.POST.get('assignedDoctorId'))
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')  # Set doctor reference
            patient.save()  # Save the patient instance

            # Add user to the 'PATIENT' group
            my_patient_group, _ = Group.objects.get_or_create(name='PATIENT')
            my_patient_group.user_set.add(user)

            # ✅ Add warning message for verification
            messages.warning(request, "Your account has been created successfully! Pending verification.")

            # print("HELLO I'm failed user")
            
            # return HttpResponseRedirect('')
            return redirect('')
    messages.error(request, "Can not add patient. Form Issued occured")
    return redirect('')
        
    # return render(request, '')

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient/patient_view_appointment.html',{'appointments':appointments,'patient':patient})


def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) 
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None
    return render(request,'hospital/patient/patient_view_doctor.html',{'patient':patient,'doctors':doctors,'role':role})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_fitness(request):
    patient=models.Patient.objects.get(user_id=request.user.id) 
    user_health = models.UserHealth.objects.filter(user=patient).first()
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None
    
    if request.method == "POST":
        # Pass instance=user_health to update existing record
        form = forms.UserHealthForm(request.POST, instance=user_health)
        if form.is_valid():
            user_health = form.save(commit=False)
            user_health.user = patient  #Link the patient
            user_health.save()
            return redirect("patient-fitness")  # Redirect after saving
    else:
        form = forms.UserHealthForm(instance=user_health)

    print(user_health)
    

    if user_health:
        bmi = calculate_bmi(user_health.height,user_health.weight)
        bmi_indicator = get_bmi_category(bmi)
        bmr = calculate_bmr(user_health.height,user_health.weight,patient.dob,patient.gender)
        tdee = calculate_tdee(bmr,user_health.activity_level)
        calories_need = calories_needed(tdee,user_health.goal)  # Can change to 'lose' or 'gain'
    else:
        bmi, bmi_indicator, bmr, tdee, calories_need= None, "No data", None, None, None    
    
    
    fitness_info={
        'bmi':bmi,
        'bmi_indicator':bmi_indicator,
        'bmr':bmr,
        'tdee':tdee,
        'calories_need':calories_need,          
    }
    
    context = {
        'age':calculate_age(patient.dob),
        'user_health_form': form,
        'patient':patient,
        'user_health': user_health,
        'fitness_info':fitness_info,
        'role':role,
    }
    return render(request,'hospital/patient/patient_fitness.html',context)


def update_userhealth(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    user_health, created = models.UserHealth.objects.get_or_create(user=patient)
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None

    if request.method == "POST":
        user_health_form = forms.UserHealthForm(request.POST, instance=user_health)  
        if user_health_form.is_valid():
            user_health_form.save()  #
            return redirect('patient-fitness')  
    else:
        user_health_form = forms.UserHealthForm(instance=user_health)  # Pre-fill form with existing data
     
    
    context = {
        'patient':patient,
        'user_health_form':user_health_form,
        'role':role,
    }
    return render(request, "hospital/patient/update_patient_health.html",context)

