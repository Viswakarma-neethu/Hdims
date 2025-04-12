from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Doctor, Patient, UserProfile

# Signup Form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # ✅ Hash password
        if commit:
            user.save()
        return user

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

# Appointment Form
"""class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        empty_label="Select a Doctor",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True  # Ensure this field is required
    )
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'symptoms', 'allergy', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }"""




class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'gender', 'symptoms', 'allergy', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'allergy': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


# Patient Form
class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.errors.get(field):
                self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender','blood_pressure', 'heart_rate', 'medical_history', 'allergies']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 4}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

# User Profile Forms
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter address'

class ProfileInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True


# class EditPatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = '__all__' 


class EditPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Patient
        fields = '__all__'
