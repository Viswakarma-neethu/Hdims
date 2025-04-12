from django.urls import path
from . import views
from .views import (
    login_view, signup, index, about, service, price, contact, 
    blog_view, search, detail_view, team_view, testimonial_view, 
    logout_view, book_appointment, submit_appointment, appointment_success, 
    patient_form_view, appointment_list, success_page, add_patient, chatbot_response, profile_view, edit_patient, monitor_appointments # ✅ Include appointment_list
)

urlpatterns = [
    path('', login_view, name='login'),
    path('index/', index, name='index'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    
    # Appointments
    path('appointment/', book_appointment, name='appointment'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('submit_appointment/', submit_appointment, name='submit_appointment'),
    path('appointment_list/', appointment_list, name='appointment_list'),  # ✅ Fixed missing URL
    path('appointment_success/<int:appointment_id>/', appointment_success, name='appointment_success'),
    path('patient_form/', views.patient_form, name='patient_form'),
    path('add_patient/', add_patient, name='add_patient'),
    path('success/', success_page, name='success_page'),
    path('submit_health_data/', views.submit_health_data, name='submit_health_data'),
    path('chatbot-response/', chatbot_response, name='chatbot_response'),
    path('profile/', profile_view, name='profile'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    path('appointment/', views.appointment_list, name='appointment_list'),
    # path('add_appointment/', views.add_appointment, name='add_appointment'),
    # path('view_appointments/', views.view_appointments, name='view_appointments'),
    # path('edit-patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    # Add these URL patterns
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patient-records/', views.patient_records, name='patient_records'),
    path('monitor_appointments/', monitor_appointments, name='monitor_appointments'),
    path('appointments/', views.user_appointments, name='user_appointments'),  # For regular users
    path('monitor_appointments/', views.monitor_appointments, name='monitor_appointments'),  # For admins
    path('view-all-appointments/', views.view_all_appointments, name='view_all_appointments'),
    # path('appointments/', views.book_appointment, name='user_appointments'),
    path('analytics/', views.analytics_view, name='analytics'),
    # path('download_report_user/', views.download_report_user, name='download_report_user'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    #path('chatbot-response/', chatbot_response, name='chatbot_response'),

    path('add_medical_history/', views.add_medical_history, name='add_medical_history'),
    path('show_medical_history/', views.show_medical_history, name='show_medical_history'),
    path('add_medical_history/', views.add_medical_history, name='add_medical_history'),

    # Other Pages
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('price/', price, name='price'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('blog/', blog_view, name='blog'),
    path('detail/', detail_view, name='detail'),
    path('team/', team_view, name='team'),
    path('testimonial/', testimonial_view, name='testimonial'),
]