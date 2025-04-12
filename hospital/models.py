# from django.db import models
# from django.conf import settings
# from django.utils import timezone
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from .managers import CustomUserManager
# from django.contrib.auth.models import User

# # User Profile Model
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

#     def __str__(self):
#         return self.user.username

# class Medication(models.Model):
#     name = models.CharField(max_length=255)
#     dosage = models.CharField(max_length=100)
#     prescribed_date = models.DateField(default=timezone.now)

# # Patient Model
# class Patient(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=255)
#     age = models.IntegerField()
#     gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])  # New field
#     blood_pressure = models.CharField(max_length=50, blank=True, null=True)
#     heart_rate = models.IntegerField(blank=True, null=True)
#     medical_history = models.TextField(blank=True, null=True)
#     allergies = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.name

# # Custom User Model
# """class CustomUser(AbstractBaseUser, PermissionsMixin):
#     id = models.BigAutoField(primary_key=True)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     def __str__(self):
#         return self.email"""

# # Signals to create a profile when a new user registers
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'userprofile'):
#         instance.userprofile.save()


# class Doctor(models.Model):
#     DEPARTMENTS = [
#         ('Cardiology', 'Cardiology'),
#         ('Neurology', 'Neurology'),
#         ('Pediatrics', 'Pediatrics'),
#         ('Orthopedics', 'Orthopedics'),
#         ('General', 'General'),
#         ('Dermatology', 'Dermatology'),
#     ]
    
#     name = models.CharField(max_length=100)
#     department = models.CharField(max_length=100, choices=DEPARTMENTS)
#     specialization = models.CharField(max_length=255)
    
#     def __str__(self):
#         return f"Dr. {self.name} ({self.department})"

# class Appointment(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     appointment_date = models.DateField()
#     appointment_time = models.TimeField()
#     gender = models.CharField(
#         max_length=10,
#         choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
#         default="Male",  # You can change the default value as needed
#     )
#     symptoms = models.TextField()
#     heart_rate = models.IntegerField(null=True, blank=True)
#     allergy = models.CharField(max_length=255, null=True, blank=True)
#     reason = models.TextField()
#     status = models.CharField(
#         max_length=20,
#         choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Canceled", "Canceled")],
#         default="Pending",
#     )
    
#     def __str__(self):
#         return f"Appointment with {self.doctor.name} on {self.appointment_date}"


from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Doctor Model
class Doctor(models.Model):
    DEPARTMENTS = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('Orthopedics', 'Orthopedics'),
        ('General', 'General'),
        ('Dermatology', 'Dermatology'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENTS)
    specialization = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Dr. {self.name} ({self.department})"


# Medication Model
class Medication(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    prescribed_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


# Patient Model
class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Appointment Model
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        default="Male",
    )
    symptoms = models.TextField()
    heart_rate = models.IntegerField(null=True, blank=True)
    allergy = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Canceled", "Canceled")],
        default="Pending",
    )

    def __str__(self):
        # return f"Appointment with {self.doctor.name} on {self.appointment_date}"
        # return f"{self.patient.name} - {self.appointment_date}"
        return f"{self.user.username} - {self.appointment_date}"


# Signals to create & save profile when a new user registers
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.patient} - {self.medical_history}"