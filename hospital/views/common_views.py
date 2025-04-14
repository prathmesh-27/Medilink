from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout,authenticate,login
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages


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