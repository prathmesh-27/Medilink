from django import forms
from django.contrib.auth.models import User
from . import models
from .models import DoctorAvailability
from datetime import date, timedelta


#Login Classes
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
  

#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }


#for Doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields=['address','mobile','department','status','gender','profile_pic']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gender': forms.Select(attrs={'class': 'form-control'}), 
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }



#for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        )
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'pattern': '[6789][0-9]{9}',
                'placeholder': 'Mobile Number'
            }
        )
    )    
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic','dob','gender']
        


class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class ContactusForm(forms.Form):
    Name = forms.CharField(
        max_length = 50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )

    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Write your message here...'
        })
    )
    

class UserHealthForm(forms.ModelForm):
    ACTIVITY_CHOICES = [
        ("sedentary", "Sedentary (Little to no exercise)"),
        ("light", "Light (1-3 days/week)"),
        ("moderate", "Moderate (3-5 days/week)"),
        ("very_active", "Very Active (6-7 days/week)"),
        ("super_active", "Super Active (Athlete or physical job)"),
    ]
    
    GOAL_CHOICES = [
        ("maintain", "Maintain Weight"),
        ("lose", "Lose Weight"),
        ("gain", "Gain Weight"),
    ]

    activity_level = forms.ChoiceField(
        choices=ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.UserHealth
        fields = ['weight', 'height', 'activity_level', 'goal']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter weight (kg)'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter height (cm)'}),
        }


class DoctorAvailabilityForm(forms.Form):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def save(self, doctor):
        """Saves availability for the next 7 days (excluding today) based on selected days."""
        today = date.today()
        availabilities = []

        # Loop through the next 7 days (excluding today)
        for i in range(1, 8):  # Only next 7 days (1 to 7)
            future_date = today + timedelta(days=i)
            day_name = future_date.strftime('%A')  # Get the day name (e.g., "Monday")

            # If this future date matches one of the selected days, save it
            if day_name in self.cleaned_data['days_of_week']:
                availability = DoctorAvailability(
                    doctor=doctor,
                    date_available=future_date,
                    day_of_week=day_name,
                    start_time=self.cleaned_data['start_time'],
                    end_time=self.cleaned_data['end_time']
                )
                availabilities.append(availability)

        # Bulk insert to optimize performance
        DoctorAvailability.objects.bulk_create(availabilities)