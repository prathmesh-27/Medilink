from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib import messages

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
    appointments=zip(appointments,patients)
    context = {
        "appointments":appointments,
        "doctor":doctor,
    }
    return render(request,'hospital/doctor/doctor_appointment.html',context)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor/doctor_dashboard.html',context=mydict)

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
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    mydict={
    'patients':patients,
    'doctor_pic':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
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

# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_view_appointment_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})

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

#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctor/doctorclick.html')

