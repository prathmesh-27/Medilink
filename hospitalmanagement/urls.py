from django.contrib import admin
from django.urls import path
from hospital.views import admin_views, doctor_views, patient_views,feature_views,authentication_views,common_views,appointment_views,misc_views,report_views
from django.contrib.auth.views import LoginView


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path("user_login/", authentication_views.user_login, name="user_login"),
    path('adminlogin', LoginView.as_view(template_name='hospital/admin/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctor/doctorlogin.html'),name = 'doctorlogin'),
    path('patientlogin', LoginView.as_view(template_name='hospital/patient/patientlogin.html')),
    path('afterlogin', authentication_views.afterlogin_view,name='afterlogin'),
    path('logout', authentication_views.logout_view,name='logout'),
    path('delete-doctor-from-hospital/<int:pk>', misc_views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('approve-doctor/<int:pk>', appointment_views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', appointment_views.reject_doctor_view,name='reject-doctor'),
    path('approve-patient/<int:pk>', appointment_views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', appointment_views.reject_patient_view,name='reject-patient'),
    path('approve-appointment/<int:pk>', appointment_views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', appointment_views.reject_appointment_view,name='reject-appointment'),
]

urlpatterns+=[
    path('',common_views.home_view,name=''),
    path('aboutus', common_views.aboutus_view),
    path('contactus', common_views.contactus_view,name="contactus"),
    path('search', common_views.search_view,name='search'),
    path('load-form/', common_views.load_form, name='load_form'),  # AJAX URL to fetch forms dynamically
    path('searchdoctor', common_views.search_doctor_view,name='searchdoctor'),
]

#---------FOR ADMIN RELATED URLS-------------------------------------
urlpatterns+=[
    path('admin-patient', admin_views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', admin_views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', misc_views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', admin_views.update_patient_view,name='update-patient'),
    path('admin-add-patient', admin_views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', admin_views.admin_approve_patient_view,name='admin-approve-patient'),
    path('admin-appointment', admin_views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', admin_views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', admin_views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', admin_views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('admin-dashboard', admin_views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-doctor', admin_views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', admin_views.admin_view_doctor_view,name='admin-view-doctor'),
    path('update-doctor/<int:pk>', admin_views.update_doctor_view,name='update-doctor'),
    # path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', admin_views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('admin-view-doctor-specialisation',admin_views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),
    path('adminsignup', admin_views.admin_signup_view,name='adminsignup'),
    path('adminclick', admin_views.adminclick_view),
    path('admin-discharge-patient',admin_views.discharge_patient_view) #To be Corrected
    
]

#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', doctor_views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor-patient', doctor_views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', doctor_views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',doctor_views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment', doctor_views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', doctor_views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',doctor_views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('doctorclick', doctor_views.doctorclick_view),
    path('doctorsignup', doctor_views.doctor_signup_view,name='doctorsignup'),
    path('delete-appointment/<int:pk>', appointment_views.delete_appointment_view,name='delete-appointment'),
]

#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', patient_views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', patient_views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', patient_views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', patient_views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', patient_views.patient_view_doctor_view,name='patient-view-doctor'),
    path('patient-discharge', patient_views.patient_discharge_view,name='patient-discharge'),
    path('patientclick', patient_views.patientclick_view),
    path('patientsignup', patient_views.patient_signup_view),

]


urlpatterns+=[
    path('download-pdf/<int:pk>', report_views.download_pdf_view,name='download-pdf'),
    path('age-pie-chart', report_views.age_pie_chart, name='age_pie_chart'),
    path('dashboard', report_views.generate_charts, name='dashboard'),
]

urlpatterns += [
    path('get-diet/',feature_views.get_diet,name='get_diet'),
    path('send-to-flask/', feature_views.send_to_flask, name='send_to_flask'),
]
