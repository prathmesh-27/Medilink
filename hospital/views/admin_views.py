from django.shortcuts import render,redirect,reverse
from hospital import forms, models
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
# from django.conf import settings
from datetime import date
from django.utils.http import urlencode


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-appointment')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin/admin_add_doctor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-patient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin/admin_approve_appointment.html',{'appointments':appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor= models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin/admin_update_doctor.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    appointments_approved= models.Appointment.objects.all().filter(status=True)
    appointments_not_approved= models.Appointment.objects.all().filter(status=False)
    appointmentForm= forms.AppointmentForm()
    context = {
        'appointments_approved': appointments_approved,
        'appointments_not_approved':appointments_not_approved,
        'appointmentForm': appointmentForm,
    }
    
    return render(request,'hospital/admin/admin_appointment.html',context)

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_approve_patient_view(request):
#     patients=models.Patient.objects.all().filter(status=False)
#     return render(request,'hospital/admin/admin_approve_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin/admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin/admin_discharge_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    doctors_approved =models.Doctor.objects.all().filter(status=True)
    doctors_not_approved = models.Doctor.objects.all().filter(status=False)
    doctors_specialization=models.Doctor.objects.all().filter(status=True)
    context={
        "doctors_approved":doctors_approved,
        "doctors_not_approved":doctors_not_approved,
        "doctors_specialization":doctors_specialization,
    }
    return render(request,'hospital/admin/admin_doctor.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    patients_approved = models.Patient.objects.all().filter(status=True)
    patients_not_approved =models.Patient.objects.all().filter(status=False)
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    context = {
        "patients_approved":patients_approved,
        "userForm":userForm,
        "patientForm":patientForm,
        "patients_not_approved":patients_not_approved,
    
    }
    return render(request,'hospital/admin/admin_patient.html',context)

def admin_signup_view(request):
    loginform = forms.LoginForm()
    signupform = forms.AdminSigupForm()
    if request.method=='POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            messages.success(request, "Admin successfully logged in!")
            return HttpResponseRedirect('/')
    return render(request,'hospital/index.html',{'loginform':loginform,'signupform':signupform})

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_appointment_view(request):
#     appointments=models.Appointment.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_view_appointment.html',{'appointments':appointments})

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_doctor_specialisation_view(request):
    
#     return render(request,'hospital/admin/admin_view_doctor_specialisation.html',{'doctors':doctors})

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_doctor_view(request):
#     doctors=models.Doctor.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin/admin_view_patient.html',{'patients':patients})

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/admin/adminclick.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin/admin_update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin/admin_discharge_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost= int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        
        # ✅ **Mark the patient as discharged**
        patient.is_discharged = True
        patient.save()
        
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notification(request):
    return render(request,'hospital/admin/admin_notification.html')
