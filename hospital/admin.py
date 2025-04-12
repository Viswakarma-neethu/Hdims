from django.contrib import admin
from .models import Doctor, Appointment, Patient, UserProfile

# Unregister first to avoid duplicate registration
#admin.site.unregister(UserProfile)  # This prevents double registration if it already exists
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(UserProfile)
