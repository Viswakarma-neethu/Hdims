from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, OuterRef, Subquery
from django.conf import settings
from .forms import SignupForm, LoginForm, AppointmentForm
from django.shortcuts import render, get_object_or_404
from .models import Doctor
from django.http import HttpResponse
from .forms import PatientForm
from .ai_assistant import analyze_health_data
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from .models import MedicalHistory
from django.db.models import Count, Avg
from .models import Patient
from django.urls import reverse
from django.http import JsonResponse
from .models import Patient, Appointment, Medication  # Import your models
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib import messages
from .forms import ProfileUpdateForm, ProfileInfoUpdateForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.core.serializers import serialize


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # If logged in, go to index page

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('index')  # Redirect to index page
            else:
                return render(request, 'hospital/login.html', {'form': form, 'error': 'Invalid credentials'})

    else:
        form = LoginForm()
    return render(request, 'hospital/login.html', {'form': form})

# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('index')  # Already logged in → Go to index

#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])  # Hash Password
#             user.save()  # This will also create UserProfile because of signals.py

#             login(request, user)  # Auto login after signup
#             messages.success(request, "Account Created Successfully!")
#             return redirect('index')
#     else:
#         form = SignupForm()

#     return render(request, 'hospital/signup.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')  # Already logged in → Go to index

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash Password
            user.save()  # Auto create profile (if signals.py used)

            login(request, user)  # Auto Login After Signup
            messages.success(request, "Account Created Successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid data. Please check and try again.")
    else:
        form = SignupForm()

    return render(request, 'hospital/signup.html', {'form': form})



@login_required(login_url='login')
def index(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'hospital/index.html', {'appointments': appointments})

def about(request):
    return render(request, 'hospital/about.html')

def service(request):
    return render(request, 'hospital/service.html')

def price(request):
    return render(request, 'hospital/price.html')

def contact(request):
    return render(request, 'hospital/contact.html')

def blog_view(request):
    return render(request, 'hospital/blog.html')  # Ensure this template exists

def search(request):
    return render(request, 'hospital/search.html')  # Ensure this template exists

def detail_view(request):
    return render(request, 'hospital/detail.html')

def team_view(request):
    return render(request, 'hospital/team.html') 

def testimonial_view(request):
    return render(request, 'hospital/testimonial.html')

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to login page after logout

def patient_form_view(request):
    return render(request, 'hospital/patient_form.html')  # Ensure this template path is correct


# views.py
@login_required
def book_appointment(request):
    # Define standard time slots
    time_slots = [
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'), 
        ('11:00', '11:00 AM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM')
    ]
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.user = request.user
                
                # Validate date is not in the past
                if appointment.appointment_date < timezone.now().date():
                    form.add_error('appointment_date', 'Date cannot be in the past')
                    raise ValueError("Past date selected")
                
                appointment.save()
                return redirect('appointment_success', appointment_id=appointment.id)
                
            except Exception as e:
                # Log error for debugging
                print(f"Error saving appointment: {str(e)}")
                messages.error(request, "An error occurred while booking your appointment")
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = AppointmentForm()
    doctors = Doctor.objects.all().select_related()
    # Organize doctors by department
    departments = Doctor.DEPARTMENTS
    doctors = Doctor.objects.all()

    return render(request, 'hospital/appointment.html', {
        'form': form,
        'doctors': doctors,
        'departments': departments,
        'time_slots': time_slots,
        'user': request.user
    })


@login_required
def appointment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    return render(request, 'hospital/appointment_success.html', {
        'appointment': appointment
    })


@login_required
def appointment_list(request):
    # Check if admin is viewing
    if request.user.is_superuser: 
        appointments = Appointment.objects.all().order_by('-appointment_date')
    else:
        appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date')

    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})


def submit_appointment(request):
    # Your function logic here
    return HttpResponse("Appointment Submitted")



def success_page(request):
    return render(request, 'hospital/success.html')


@login_required
def patient_list(request):
    patients = Patient.objects.filter(user=request.user)  # Only logged-in user patients
    return render(request, 'patient_list.html', {'patients': patients})



def patient_form(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form})



def submit_health_data(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        age = request.POST.get('age')
        blood_pressure = request.POST.get('blood_pressure')
        heart_rate = request.POST.get('heart_rate')
        medical_history = request.POST.get('medical_history')
        allergies = request.POST.get('allergies')
        return HttpResponse("Health data submitted successfully!")  # Temporary response
    return redirect('patient_form')  # Redirect back to the form if accessed directly


def submit_health_data(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            patient_data = {
                'name': patient.name,
                'age': patient.age,
                'blood_pressure': patient.blood_pressure,
                'heart_rate': patient.heart_rate,
                'medical_history': patient.medical_history,
                'allergies': patient.allergies,
            }
            advice = analyze_health_data(patient_data)

            return render(request, 'hospital/health_advice.html', {'advice': advice, 'patient': patient})

    return redirect('patient_form')

def index(request):
    # Initialize variables
    # latest_patient = Patient.objects.last)
    latest_patient = Patient.objects.last()  # Get the most recent patient

    if not latest_patient:
        latest_patient = None  # Explicitly set it to None if no patients exist
    health_advice = []
    patients = Patient.objects.all() 
    if latest_patient:
        patient_data = {
            'blood_pressure': latest_patient.blood_pressure,
            'heart_rate': latest_patient.heart_rate,
            'medical_history': latest_patient.medical_history,
            'allergies': latest_patient.allergies,
        }
        health_advice = analyze_health_data(patient_data) if patient_data else []
    appointments = None  # Default value

    if request.user.is_staff:  # Check if the user is an admin
        appointments = Appointment.objects.all()  # Fetch all appointments for admin
    return render(request, 'hospital/index.html', {
        'health_advice': health_advice,
        'latest_patient': latest_patient,
        'patients':patients,
        'appointments':appointments  # Make sure this is passed
    })


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message", "").lower()  # Get user input
            
            # Default Response
            bot_response = "I'm sorry, I didn't understand that. Please ask me about health advice, your appointments, or medications."

            # Health Advice
            if "symptoms of" in user_message:
                disease = user_message.replace("symptoms of", "").strip()
                health_tips = {
                    "diabetes": "Symptoms include frequent urination, thirst, and weight loss.",
                    "hypertension": "Symptoms include headaches, dizziness, and blurred vision.",
                }
                bot_response = health_tips.get(disease, "I'm not sure about that disease. Please consult a doctor.")

            # Fetch Patient Data
            elif "my details" in user_message:
                patient = Patient.objects.filter(user=request.user).first()  # ✅ Use logged-in user
                if patient:
                    bot_response = f"Your details: Name - {patient.name}, Age - {patient.age}, Condition - {patient.condition}"
                else:
                     bot_response = "Patient record not found."

            # Check Appointments
            elif "my appointment" in user_message:
                appointment = Appointment.objects.filter(patient_name="John Doe").first()
                if appointment:
                    bot_response = f"Your appointment is on {appointment.date} with Dr. {appointment.doctor}."
                else:
                    bot_response = "No upcoming appointments found."

            # Medication Reminders
            elif "my medication" in user_message:
                medications = Medication.objects.filter(patient_name="John Doe")
                if medications.exists():
                    med_list = ", ".join([med.name for med in medications])
                    bot_response = f"Your prescribed medications: {med_list}."
                else:
                    bot_response = "No medications found in your record."

            # Send Response
            return JsonResponse({"response": bot_response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid request format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def profile_view(request):
    # Check if profile exists; if not, set `profile` to None
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'hospital/profile.html', context)

# def edit_profile(request):
#     return render(request, "hospital/edit_profile.html")



@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')

        request.user.save()
        profile.save()

        messages.success(request, "Profile Updated Successfully!")
        return redirect('profile')

    return render(request, 'hospital/edit_profile.html')



@login_required
def edit_profile(request):
    user = request.user  # Get the logged-in user
    profile, created = UserProfile.objects.get_or_create(user=user)  # Assuming you have a related Profile model

    if request.method == "POST":
        user_form = ProfileUpdateForm(request.POST, instance=user)
        profile_form = ProfileInfoUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.instance.username = user.username  # Ensure username is unchanged
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')  # Redirect to profile page

    else:
        user_form = ProfileUpdateForm(instance=user)
        profile_form = ProfileInfoUpdateForm(instance=profile)

    return render(request, 'hospital/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after saving
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'hospital/profile.html', {'form': form})


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']

            # Check if patient already exists
            patient = Patient.objects.filter(name=name, age=age, gender=gender).first()
            if patient:
                #messages.warning(request, "This patient already exists. You can edit their record.")
                return redirect(reverse('edit_patient', kwargs={'patient_id': patient.id}))

            # Save new patient if unique
            patient = form.save()
            #messages.success(request, "Patient created successfully!")
            return redirect(reverse('patient_detail', kwargs={'patient_id': patient.id}))

    else:
        form = PatientForm()

    return render(request, 'hospital/patient_form.html', {'form': form})




def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'hospital/patient_detail.html', {'patient': patient})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully!")
            return redirect(reverse('patient_detail', kwargs={'patient_id': patient.id}))
    else:
        form = PatientForm(instance=patient)

    return render(request, 'hospital/edit_patient_form.html', {'form': form, 'patient': patient})


def is_admin(user):
    return user.is_staff

@login_required
def patient_list(request):
    return render(request, 'hospital/patient_records.html')  # Normal users

@login_required
def patient_records(request):
    if request.user.is_staff:  # Only admins can see all patients
        patients = Patient.objects.order_by('id', 'created_at')  # Fetch all patients
        unique_patients = {patient.id: patient for patient in patients}.values()  # Remove duplicates
        return render(request, 'hospital/patient_records.html', {'patients': unique_patients})
    else:
        return redirect('your_profile_view')  # Redirect normal users to profile


def monitor_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'hospital/monitor_appointments.html', {'appointments': appointments})


@login_required
def user_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date')
    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments
    })


def view_all_appointments(request):
    if request.user.is_staff:  # Only admin can access
        appointments = Appointment.objects.all()
        return render(request, 'hospital/view_all_appointments.html', {'appointments': appointments})
    else:
        return redirect('login')  # Redirect non-admin users


@login_required
def analytics_view(request):
    if request.user.is_staff:  # Admin View
        total_patients = Patient.objects.count()
        total_appointments = Appointment.objects.count()

        # Top Diseases from MedicalHistory
        top_diseases = MedicalHistory.objects.values('disease').annotate(count=Count('disease')).order_by('-count')

        # Analytics based on medical history from Patient table (if exists)
        medical_history_data = Patient.objects.values('medical_history').annotate(count=Count('medical_history'))

        # Analytics based on gender
        gender_data = Patient.objects.values('gender').annotate(count=Count('gender'))

        # Analytics based on age group
        age_groups = {
            '0-18': Patient.objects.filter(age__range=(0, 18)).count(),
            '19-35': Patient.objects.filter(age__range=(19, 35)).count(),
            '36-60': Patient.objects.filter(age__range=(36, 60)).count(),
            '60+': Patient.objects.filter(age__gte=61).count(),
        }

        context = {
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'top_diseases': top_diseases,
            'medical_history_data': medical_history_data,
            'gender_data': gender_data,
            'age_groups': age_groups,
        }
        return render(request, 'hospital/staff_dashboard.html', context)

    else:  # Normal User View
        patient = Patient.objects.filter(user=request.user).first()
        appointments = Appointment.objects.filter(user=request.user)

        context = {
            'patient': patient,
            'appointments': appointments,
        }
        return render(request, 'hospital/user_dashboard.html', context)
    

@login_required
def add_medical_history(request):
    # Check patient exists or not
    patient, created = Patient.objects.get_or_create(user=request.user, defaults={
        'name': request.user.username,
        'age': 0,  # default age, change as needed
        'gender': 'Male'  # default gender, change as needed
    })

    if request.method == 'POST':
        disease = request.POST.get('disease')
        description = request.POST.get('description')
        date = request.POST.get('date')

        MedicalHistory.objects.create(
            patient=patient,
            disease=disease,
            description=description,
            date=date,
        )

        messages.success(request, "Medical History Added Successfully!")
        return redirect('show_medical_history')

    return render(request, 'hospital/add_medical_history.html')



# Show Medical History View
@login_required
def show_medical_history(request):
    patient = Patient.objects.get(user=request.user)
    medical_history = MedicalHistory.objects.filter(patient=patient)

    context = {
        'medical_history': medical_history
    }
    return render(request, 'hospital/show_medical_history.html', context)

