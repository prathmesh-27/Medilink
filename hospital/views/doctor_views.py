from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import localdate

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=list(zip(appointments,patients))
    
    context = {
        "appointments":appointments,
        "doctor":doctor,
        "role":request.user.groups.first().name.title() if request.user.groups.exists() else None
    }
    return render(request,'hospital/doctor/doctor_appointment.html',context)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)

def doctor_dashboard_view(request):
    # For the three dashboard cards
    patientcount = models.Patient.objects.filter(
        status=True, assignedDoctorId=request.user.id, is_discharged=False
    ).count()
    
    appointmentcount = models.Appointment.objects.filter(status=True, doctorId=request.user.id).count()
    
    patientdischarged = models.PatientDischargeDetails.objects.filter(assignedDoctorName=request.user.first_name).distinct().count()
    
    role = request.user.groups.first().name.title() if request.user.groups.exists() else None

    # Get today's date
    today = localdate()

    # Today's Appointments
    today_appointments = models.Appointment.objects.filter(
        status=True, 
        doctorId=request.user.id, 
        appointmentDate=today
    ).order_by('-id')

    today_patient_ids = [a.patientId for a in today_appointments]

    today_patients = models.Patient.objects.filter(
        status=True, 
        user_id__in=today_patient_ids
    ).order_by('-id')

    today_appointments = zip(today_appointments, today_patients)

    # Upcoming Appointments (Appointments after today)
    upcoming_appointments = models.Appointment.objects.filter(
        status=True, 
        doctorId=request.user.id, 
        appointmentDate__gt=today  # Future dates
    ).order_by('appointmentDate')

    upcoming_patient_ids = [a.patientId for a in upcoming_appointments]

    upcoming_patients = models.Patient.objects.filter(
        status=True, 
        user_id__in=upcoming_patient_ids
    ).order_by('-id')

    upcoming_appointments = zip(upcoming_appointments, upcoming_patients)

    # Prepare data for the template
    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # Doctor profile pic in sidebar
        'role': role,
    }

    return render(request, 'hospital/doctor/doctor_dashboard.html', context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id,is_discharged = False)
    discharged_patient = models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id,is_discharged = True)
    
    mydict={
    'doctor':doctor,
    'patients':patients,
    'doctor_pic':models.Doctor.objects.get(user_id=request.user.id),
    'role' :request.user.groups.first().name.title() if request.user.groups.exists() else None,
    'discharged_patient':discharged_patient,
    }
    return render(request,'hospital/doctor/doctor_patient.html',context=mydict)

def doctor_signup_view(request):
    doctorForm = forms.DoctorForm()
    userForm = forms.DoctorUserForm()
    signupform = {"doctor":doctorForm,"user":userForm}
    loginform = forms.LoginForm()
    # print(signupform)
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user= userForm.save(commit=False)
            user.set_password(user.password)
            user.save()
            doctor= doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.warning(request, "Doctor Registered Successfully. Wait For Admin Approval")
            # print("Doctor Registered Successfully")
        return HttpResponseRedirect('/')
    
    return render(request,'hospital/index.html',{'loginform':loginform,'signupform':signupform})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) 
    return render(request,'hospital/doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_availability(request):
    if request.method == "POST":
        availabilityform = forms.DoctorAvailabilityForm(request.POST)
        if availabilityform.is_valid():
            availabilityform.save(doctor=request.user.doctor)  # Assuming logged-in user is a doctor
            return redirect('doctor-availability')  # Redirect to success page

    else:
        availabilityform = forms.DoctorAvailabilityForm()
        
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    # Fetch all availability records for this doctor
    availabilities = models.DoctorAvailability.objects.filter(doctor=doctor).order_by('date_available')
    
    if request.method == "POST" and "reset" in request.POST:
        # Delete all availability records for the current doctor
        availabilities.delete()
        return redirect('doctor-availability')
    
    context = {
        'doctor': doctor,
        'availabilities': availabilities, 
        'availabilityform':availabilityform,
        'role' :request.user.groups.first().name.title() if request.user.groups.exists() else None
    }
    return render(request, 'hospital/doctor/doctor_availability.html', context)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def reset_availability(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})


