from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


departments = [
    ('Cardiologist', 'Cardio'),
    ('Dermatologists', 'Derma'),
    ('Allergists', 'Allergy'),
    ('General Surgery', 'Gen Surg'),
    ('Pediatricians', 'Pedia'),
    ('Orthopedic Surgeons', 'Ortho'),
    ('Neurologists', 'Neuro'),
    ('Psychiatrists', 'Psych'),
    ('Gynecologists', 'Gynae'),
    ('Endocrinologists', 'Endo')
]


# Gender Choices (Defined Outside the Model)
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

# Appointment Day Choices
DAY_CHOICES = [
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
]



class Doctor(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, default='Male')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    status=models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    is_emergency = models.BooleanField(default=False)
    is_discharged = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    appointment_day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)
    
    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date_available = models.DateField(default=now) 
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Availability - {self.doctor} on {self.day_of_week}"  
    

ACTIVITY_LEVELS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "very_active": 1.725,
    "super_active": 1.9,
}    
      

class UserHealth(models.Model):
    GOAL_CHOICES = [
        ("maintain", "Maintain Weight"),
        ("lose", "Lose Weight"),
        ("gain", "Gain Weight"),
    ]
    
    user = models.ForeignKey('Patient', on_delete=models.CASCADE, null=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(
        max_length=20, 
        choices=[(k, k.replace("_", " ").title()) for k in ACTIVITY_LEVELS.keys()],
        default="sedentary"
    )
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default="maintain")

    
    def __str__(self):
        return f"UserHealth - {self.user}"

