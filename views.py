# from django.shortcuts import render,redirect,reverse
# from . import forms,models
# from django.db.models import Sum
# from django.contrib.auth.models import Group
# from django.http import HttpResponseRedirect
# from django.core.mail import send_mail
# from django.contrib.auth.decorators import login_required,user_passes_test
# from django.contrib.auth import logout,authenticate,login
# from datetime import datetime,timedelta,date
# from django.conf import settings
# from django.db.models import Q


# def logout_view(request):
#     logout(request)  # Logs out the user
#     return redirect('')

# def home_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     loginform = forms.LoginForm()
#     signupform = forms.AdminSigupForm()
#     return render(request,'hospital/index.html',{'loginform':loginform,'signupform':signupform})


# #for showing signup/login button for admin
# def adminclick_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'hospital/admin/adminclick.html')


# #for showing signup/login button for doctor
# def doctorclick_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'hospital/doctor/doctorclick.html')


# #for showing signup/login button for patient
# def patientclick_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'hospital/patient/patientclick.html')



# def admin_signup_view(request):
#     form= forms.AdminSigupForm()
#     if request.method=='POST':
#         form=forms.AdminSigupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             my_admin_group = Group.objects.get_or_create(name='ADMIN')
#             my_admin_group[0].user_set.add(user)
#             return HttpResponseRedirect('adminlogin')
#     return render(request,'hospital/admin/adminsignup.html',{'form':form})


# def doctor_signup_view(request):
#     userForm=forms.DoctorUserForm()
#     doctorForm=forms.DoctorForm()
#     mydict={'userForm':userForm,'doctorForm':doctorForm}
#     if request.method=='POST':
#         userForm=forms.DoctorUserForm(request.POST)
#         doctorForm=forms.DoctorForm(request.POST,request.FILES)
#         if userForm.is_valid() and doctorForm.is_valid():
#             user= userForm.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             doctor= doctorForm.save(commit=False)
#             doctor.user=user
#             doctor=doctor.save()
#             my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#             my_doctor_group[0].user_set.add(user)
#         return HttpResponseRedirect('doctorlogin')
#     return render(request,'hospital/doctor/doctorsignup.html',context=mydict)


# def patient_signup_view(request):
#     userForm=forms.PatientUserForm()
#     patientForm=forms.PatientForm()
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST)
#         patientForm=forms.PatientForm(request.POST,request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             patient=patientForm.save(commit=False)
#             patient.user=user
#             patient.assignedDoctorId=request.POST.get('assignedDoctorId')
#             patient=patient.save()
#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)
#         return HttpResponseRedirect('patientlogin')
#     return render(request,'hospital/patient/patientsignup.html',context=mydict)






# #-----------for checking user is doctor , patient or admin
# def is_admin(user):
#     return user.groups.filter(name='ADMIN').exists()
# def is_doctor(user):
#     return user.groups.filter(name='DOCTOR').exists()
# def is_patient(user):
#     return user.groups.filter(name='PATIENT').exists()


# #---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
# def afterlogin_view(request):
#     if is_admin(request.user):
#         return redirect('admin-dashboard')
    
#     elif is_doctor(request.user):
#         accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return redirect('doctor-dashboard')
#         else:
#             return render(request,'hospital/doctor/doctor_wait_for_approval.html',{'title': 'Wait For Approval'})
#     elif is_patient(request.user):
#         accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return redirect('patient-dashboard')
#         else:
#             return render(request,'hospital/patient/patient_wait_for_approval.html')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_dashboard_view(request):
#     #for both table in admin dashboard
#     doctors=models.Doctor.objects.all().order_by('-id')
#     patients=models.Patient.objects.all().order_by('-id')
    
#     #for three cards
#     doctorcount=models.Doctor.objects.all().filter(status=True).count()
#     pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

#     patientcount=models.Patient.objects.all().filter(status=True).count()
#     pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

#     appointmentcount=models.Appointment.objects.all().filter(status=True).count()
#     pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
#     mydict={
#     'doctors':doctors,
#     'patients':patients,
#     'doctorcount':doctorcount,
#     'pendingdoctorcount':pendingdoctorcount,
#     'patientcount':patientcount,
#     'pendingpatientcount':pendingpatientcount,
#     'appointmentcount':appointmentcount,
#     'pendingappointmentcount':pendingappointmentcount,
#     }
#     return render(request,'hospital/admin/admin_dashboard.html',context=mydict)


# # this view for sidebar click on admin page
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_doctor_view(request):
#     return render(request,'hospital/admin/admin_doctor.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_doctor_view(request):
#     doctors=models.Doctor.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_view_doctor.html',{'doctors':doctors})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def delete_doctor_from_hospital_view(request,pk):
#     doctor=models.Doctor.objects.get(id=pk)
#     user=models.User.objects.get(id=doctor.user_id)
#     user.delete()
#     doctor.delete()
#     return redirect('admin-view-doctor')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def update_doctor_view(request,pk):
#     doctor=models.Doctor.objects.get(id=pk)
#     user=models.User.objects.get(id=doctor.user_id)

#     userForm=forms.DoctorUserForm(instance=user)
#     doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
#     mydict={'userForm':userForm,'doctorForm':doctorForm}
#     if request.method=='POST':
#         userForm=forms.DoctorUserForm(request.POST,instance=user)
#         doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
#         if userForm.is_valid() and doctorForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             doctor=doctorForm.save(commit=False)
#             doctor.status=True
#             doctor.save()
#             return redirect('admin-view-doctor')
#     return render(request,'hospital/admin/admin_update_doctor.html',context=mydict)




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_doctor_view(request):
#     userForm=forms.DoctorUserForm()
#     doctorForm=forms.DoctorForm()
#     mydict={'userForm':userForm,'doctorForm':doctorForm}
#     if request.method=='POST':
#         userForm=forms.DoctorUserForm(request.POST)
#         doctorForm=forms.DoctorForm(request.POST, request.FILES)
#         if userForm.is_valid() and doctorForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()

#             doctor=doctorForm.save(commit=False)
#             doctor.user=user
#             doctor.status=True
#             doctor.save()

#             my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#             my_doctor_group[0].user_set.add(user)

#         return HttpResponseRedirect('admin-view-doctor')
#     return render(request,'hospital/admin/admin_add_doctor.html',context=mydict)




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_approve_doctor_view(request):
#     #those whose approval are needed
#     doctors = models.Doctor.objects.all().filter(status=False)
#     return render(request,'hospital/admin/admin_approve_doctor.html',{'doctors':doctors})


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def approve_doctor_view(request,pk):
#     doctor= models.Doctor.objects.get(id=pk)
#     doctor.status=True
#     doctor.save()
#     return redirect(reverse('admin-approve-doctor'))


# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def reject_doctor_view(request,pk):
#     doctor=models.Doctor.objects.get(id=pk)
#     user=models.User.objects.get(id=doctor.user_id)
#     user.delete()
#     doctor.delete()
#     return redirect('admin-approve-doctor')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_doctor_specialisation_view(request):
#     doctors=models.Doctor.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_view_doctor_specialisation.html',{'doctors':doctors})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_patient_view(request):
#     return render(request,'hospital/admin/admin_patient.html')






# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def delete_patient_from_hospital_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     user=models.User.objects.get(id=patient.user_id)
#     user.delete()
#     patient.delete()
#     return redirect('admin-view-patient')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def update_patient_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     user=models.User.objects.get(id=patient.user_id)

#     userForm=forms.PatientUserForm(instance=user)
#     patientForm=forms.PatientForm(request.FILES,instance=patient)
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST,instance=user)
#         patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             patient=patientForm.save(commit=False)
#             patient.status=True
#             patient.assignedDoctorId=request.POST.get('assignedDoctorId')
#             patient.save()
#             return redirect('admin-view-patient')
#     return render(request,'hospital/admin/admin_update_patient.html',context=mydict)





# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_patient_view(request):
#     userForm=forms.PatientUserForm()
#     patientForm=forms.PatientForm()
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.PatientUserForm(request.POST)
#         patientForm=forms.PatientForm(request.POST,request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()

#             patient=patientForm.save(commit=False)
#             patient.user=user
#             patient.status=True
#             patient.assignedDoctorId=request.POST.get('assignedDoctorId')
#             patient.save()

#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)

#         return HttpResponseRedirect('admin-view-patient')
#     return render(request,'hospital/admin/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_approve_patient_view(request):
#     #those whose approval are needed
#     patients=models.Patient.objects.all().filter(status=False)
#     return render(request,'hospital/admin/admin_approve_patient.html',{'patients':patients})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def approve_patient_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     patient.status=True
#     patient.save()
#     return redirect(reverse('admin-approve-patient'))



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def reject_patient_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     user=models.User.objects.get(id=patient.user_id)
#     user.delete()
#     patient.delete()
#     return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_discharge_patient_view(request):
#     patients=models.Patient.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_discharge_patient.html',{'patients':patients})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def discharge_patient_view(request,pk):
#     patient=models.Patient.objects.get(id=pk)
#     days=(date.today()-patient.admitDate) #2 days, 0:00:00
#     assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
#     d=days.days # only how many day that is 2
#     patientDict={
#         'patientId':pk,
#         'name':patient.get_name,
#         'mobile':patient.mobile,
#         'address':patient.address,
#         'symptoms':patient.symptoms,
#         'admitDate':patient.admitDate,
#         'todayDate':date.today(),
#         'day':d,
#         'assignedDoctorName':assignedDoctor[0].first_name,
#     }
#     if request.method == 'POST':
#         feeDict ={
#             'roomCharge':int(request.POST['roomCharge'])*int(d),
#             'doctorFee':request.POST['doctorFee'],
#             'medicineCost' : request.POST['medicineCost'],
#             'OtherCharge' : request.POST['OtherCharge'],
#             'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
#         }
#         patientDict.update(feeDict)
#         #for updating to database patientDischargeDetails (pDD)
#         pDD=models.PatientDischargeDetails()
#         pDD.patientId=pk
#         pDD.patientName=patient.get_name
#         pDD.assignedDoctorName=assignedDoctor[0].first_name
#         pDD.address=patient.address
#         pDD.mobile=patient.mobile
#         pDD.symptoms=patient.symptoms
#         pDD.admitDate=patient.admitDate
#         pDD.releaseDate=date.today()
#         pDD.daySpent=int(d)
#         pDD.medicineCost=int(request.POST['medicineCost'])
#         pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
#         pDD.doctorFee=int(request.POST['doctorFee'])
#         pDD.OtherCharge=int(request.POST['OtherCharge'])
#         pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
#         pDD.save()
#         return render(request,'hospital/patient_final_bill.html',context=patientDict)
#     return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
# import io
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return



# def download_pdf_view(request,pk):
#     dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
#     dict={
#         'patientName':dischargeDetails[0].patientName,
#         'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
#         'address':dischargeDetails[0].address,
#         'mobile':dischargeDetails[0].mobile,
#         'symptoms':dischargeDetails[0].symptoms,
#         'admitDate':dischargeDetails[0].admitDate,
#         'releaseDate':dischargeDetails[0].releaseDate,
#         'daySpent':dischargeDetails[0].daySpent,
#         'medicineCost':dischargeDetails[0].medicineCost,
#         'roomCharge':dischargeDetails[0].roomCharge,
#         'doctorFee':dischargeDetails[0].doctorFee,
#         'OtherCharge':dischargeDetails[0].OtherCharge,
#         'total':dischargeDetails[0].total,
#     }
#     return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_appointment_view(request):
#     return render(request,'hospital/admin/admin_appointment.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_appointment_view(request):
#     appointments=models.Appointment.objects.all().filter(status=True)
#     return render(request,'hospital/admin/admin_view_appointment.html',{'appointments':appointments})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_appointment_view(request):
#     appointmentForm=forms.AppointmentForm()
#     mydict={'appointmentForm':appointmentForm,}
#     if request.method=='POST':
#         appointmentForm=forms.AppointmentForm(request.POST)
#         if appointmentForm.is_valid():
#             appointment=appointmentForm.save(commit=False)
#             appointment.doctorId=request.POST.get('doctorId')
#             appointment.patientId=request.POST.get('patientId')
#             appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
#             appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
#             appointment.status=True
#             appointment.save()
#         return HttpResponseRedirect('admin-view-appointment')
#     return render(request,'hospital/admin/admin_add_appointment.html',context=mydict)



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_approve_appointment_view(request):
#     #those whose approval are needed
#     appointments=models.Appointment.objects.all().filter(status=False)
#     return render(request,'hospital/admin/admin_approve_appointment.html',{'appointments':appointments})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def approve_appointment_view(request,pk):
#     appointment=models.Appointment.objects.get(id=pk)
#     appointment.status=True
#     appointment.save()
#     return redirect(reverse('admin-approve-appointment'))



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def reject_appointment_view(request,pk):
#     appointment=models.Appointment.objects.get(id=pk)
#     appointment.delete()
#     return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_dashboard_view(request):
    
#     #for three cards
#     patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
#     appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
#     patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

#     #for  table in doctor dashboard
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
#     appointments=zip(appointments,patients)
#     mydict={
#     'patientcount':patientcount,
#     'appointmentcount':appointmentcount,
#     'patientdischarged':patientdischarged,
#     'appointments':appointments,
#     'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
#     }
#     return render(request,'hospital/doctor/doctor_dashboard.html',context=mydict)



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_patient_view(request):
#     mydict={
#     'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
#     }
#     return render(request,'hospital/doctor/doctor_patient.html',context=mydict)





# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_view_patient_view(request):
#     patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def search_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
#     return render(request,'hospital/doctor/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_view_discharge_patient_view(request):
#     dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/doctor/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_appointment_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/doctor/doctor_appointment.html',{'doctor':doctor})



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



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def doctor_delete_appointment_view(request):
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def delete_appointment_view(request,pk):
#     appointment=models.Appointment.objects.get(id=pk)
#     appointment.delete()
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_dashboard_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id)
#     doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
#     mydict={
#     'patient':patient,
#     'doctorName':doctor.get_name,
#     'doctorMobile':doctor.mobile,
#     'doctorAddress':doctor.address,
#     'symptoms':patient.symptoms,
#     'doctorDepartment':doctor.department,
#     'admitDate':patient.admitDate,
#     }
#     return render(request,'hospital/patient_dashboard.html',context=mydict)



# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_appointment_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     return render(request,'hospital/patient_appointment.html',{'patient':patient})



# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_book_appointment_view(request):
#     appointmentForm=forms.PatientAppointmentForm()
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     message=None
#     mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
#     if request.method=='POST':
#         appointmentForm=forms.PatientAppointmentForm(request.POST)
#         if appointmentForm.is_valid():
#             print(request.POST.get('doctorId'))
#             desc=request.POST.get('description')

#             doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
#             appointment=appointmentForm.save(commit=False)
#             appointment.doctorId=request.POST.get('doctorId')
#             appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
#             appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
#             appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
#             appointment.status=False
#             appointment.save()
#         return HttpResponseRedirect('patient-view-appointment')
#     return render(request,'hospital/patient_book_appointment.html',context=mydict)



# def patient_view_doctor_view(request):
#     doctors=models.Doctor.objects.all().filter(status=True)
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



# def search_doctor_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
#     return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_view_appointment_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
#     return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_discharge_view(request):
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
#     patientDict=None
#     if dischargeDetails:
#         patientDict ={
#         'is_discharged':True,
#         'patient':patient,
#         'patientId':patient.id,
#         'patientName':patient.get_name,
#         'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
#         'address':patient.address,
#         'mobile':patient.mobile,
#         'symptoms':patient.symptoms,
#         'admitDate':patient.admitDate,
#         'releaseDate':dischargeDetails[0].releaseDate,
#         'daySpent':dischargeDetails[0].daySpent,
#         'medicineCost':dischargeDetails[0].medicineCost,
#         'roomCharge':dischargeDetails[0].roomCharge,
#         'doctorFee':dischargeDetails[0].doctorFee,
#         'OtherCharge':dischargeDetails[0].OtherCharge,
#         'total':dischargeDetails[0].total,
#         }
#         print(patientDict)
#     else:
#         patientDict={
#             'is_discharged':False,
#             'patient':patient,
#             'patientId':request.user.id,
#         }
#     return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# def aboutus_view(request):
#     return render(request,'hospital/other/aboutus.html',{'title': 'About Us'})

# def contactus_view(request):
#     sub = forms.ContactusForm()
#     if request.method == 'POST':
#         sub = forms.ContactusForm(request.POST)
#         if sub.is_valid():
#             email = sub.cleaned_data['Email']
#             name=sub.cleaned_data['Name']
#             message = sub.cleaned_data['Message']
#             send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
#             return render(request, 'hospital/other/contactussuccess.html')
        
#     return render(request, 'hospital/other/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#Graphs 
# def age_pie_chart(request):
#     # Sample user ages (hardcoded)
#     sample_ages = [15, 22, 35, 55, 29, 42, 18, 33, 26, 50, 17, 45, 60, 39, 23, 41, 20, 30]

#     # Categorize ages
#     age_groups = {
#         "0-18": 0,
#         "19-30": 0,
#         "31-50": 0,
#         "51+": 0
#     }

#     for age in sample_ages:
#         if age <= 18:
#             age_groups["0-18"] += 1
#         elif age <= 30:
#             age_groups["19-30"] += 1
#         elif age <= 50:
#             age_groups["31-50"] += 1
#         else:
#             age_groups["51+"] += 1

#     # Create a Plotly pie chart
#     fig = px.pie(
#         names=age_groups.keys(),
#         values=age_groups.values(),
#         title="User Age Distribution",
#     )
    
#     # Convert the chart to HTML
#     graph = fig.to_html(full_html=False)

#     return render(request, 'hospital/other/try.html', {'graph': graph})


# def generate_charts(request):
#     # Sample user ages
#     sample_ages = [15, 22, 35, 55, 29, 42, 18, 33, 26, 50, 17, 45, 60, 39, 23, 41, 20, 30]

#     # Categorize ages
#     age_groups = {"0-18": 0, "19-30": 0, "31-50": 0, "51+": 0}
#     for age in sample_ages:
#         if age <= 18:
#             age_groups["0-18"] += 1
#         elif age <= 30:
#             age_groups["19-30"] += 1
#         elif age <= 50:
#             age_groups["31-50"] += 1
#         else:
#             age_groups["51+"] += 1

#     # 📊 Bar Chart (User Age Groups)
#     bar_fig = go.Figure([go.Bar(x=list(age_groups.keys()), y=list(age_groups.values()), marker_color='blue')])
#     bar_chart = bar_fig.to_html(full_html=False, include_plotlyjs='cdn')

#     # 🥧 Pie Chart (User Age Distribution)
#     pie_fig = go.Figure([go.Pie(labels=list(age_groups.keys()), values=list(age_groups.values()))])
#     pie_chart = pie_fig.to_html(full_html=False, include_plotlyjs='cdn')

#     # 🌍 Map Graph (Random User Locations)
#     locations = pd.DataFrame({
#         "latitude": [random.uniform(-90, 90) for _ in range(10)],
#         "longitude": [random.uniform(-180, 180) for _ in range(10)]
#     })
#     map_fig = px.scatter_geo(locations, lat="latitude", lon="longitude", title="User Locations (Random)")
#     map_chart = map_fig.to_html(full_html=False, include_plotlyjs='cdn')

#     return render(request, 'hospital/other/try.html', {
#         'pie_chart': pie_chart,
#         'bar_chart': bar_chart,
#         'map_chart': map_chart
#     })
    
    
# def load_form(request):
#     form_type = request.GET.get('form_type')
#     loginform = forms.LoginForm()
    
#     if form_type == "admin":
#         signupform = forms.AdminSigupForm()
#         template = "hospital/dummy/admin_form.html"
        
#     elif form_type == "doctor":
#         doctorForm = forms.DoctorForm()
#         userForm = forms.DoctorUserForm()
#         signupform = {"doctor":doctorForm,"user":userForm}
#         print(signupform)
#         template = "hospital/dummy/doctor_form.html"

#     elif form_type == "patient":
#         patientForm = forms.PatientForm()
#         userForm = forms.PatientUserForm()
#         signupform = {"patient":patientForm,"user":userForm}
#         template = "hospital/dummy/patient_form.html"

#     else:
#         return render(request, "hospital/error.html", {"message": "Invalid form type"})
    
#     # print(signupform)
#     return render(request, template, {"loginform": loginform ,"signupform": signupform})


# def user_login(request):
#     if request.method == "POST":
#         loginform = forms.LoginForm(request.POST)
#         if loginform.is_valid():
#             username = loginform.cleaned_data["username"]
#             password = loginform.cleaned_data["password"]
#             user = authenticate(request, username=username, password=password)  # Check credentials
#             print()
#             if user is not None:
#                 login(request, user)  # Log the user in
#                 return redirect("afterlogin")  # Redirect to some page after login
#             else:
#                 return render(request, "hospital/index.html", {"loginform": loginform, "error": "Invalid credentials"})

#     else:
#         loginform = forms.LoginForm()

#     return render(request, "hospital/index.html", {"loginform": loginform})


# import requests
# from django.shortcuts import render
# from django.http import JsonResponse

# def send_to_flask(request):
#     response_data = None  # Default empty response
#     error_message = None   # Store any error messages
    
#     if request.method == 'POST':
#         name = request.POST.get("name")
#         flask_url = "http://127.0.0.1:5000/process-data"

#         try:
#             response = requests.post(flask_url, json={"name": name}, timeout=5)  # Set timeout
#             response.raise_for_status()  # Raise error for 4xx/5xx responses
            
#             response_data = response.json()  # Get processed data from Flask
#         except requests.Timeout:
#             error_message = "The server took too long to respond. Please try again later."
#         except requests.ConnectionError:
#             error_message = "Could not connect to the server. Please check your connection."
#         except requests.HTTPError as err:
#             error_message = f"API returned an error: {err.response.status_code}"
#         except Exception as e:
#             error_message = f"Something went wrong: {str(e)}"

#     return render(request, 'hospital/example.html', {"response_data": response_data, "error_message": error_message})


