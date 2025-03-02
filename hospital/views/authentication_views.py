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


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('')

#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def user_login(request):
    if request.method == "POST":
        loginform = forms.LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data["username"]
            password = loginform.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)  # Check credentials
            print()
            if user is not None:
                login(request, user)  # Log the user in
                return redirect("afterlogin")  # Redirect to some page after login
            else:
                return render(request, "hospital/index.html", {"loginform": loginform, "error": "Invalid credentials"})

    else:
        loginform = forms.LoginForm()

    return render(request, "hospital/index.html", {"loginform": loginform})



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor/doctor_wait_for_approval.html',{'title': 'Wait For Approval'})
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient/patient_wait_for_approval.html')
        
        