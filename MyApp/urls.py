from django.contrib import admin
from django.urls import path
from MyApp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import logout_view
from .views import user_landing
from .views import view_user_complaints
from .views import file_complaint
from .views import admindashboard
from .views import user_account
from .views import generate_pdf
from .views import missing_person_list, report_missing_person, missing_person_lista, missing_person_details
from .views import police_home
from .views import most_wanted_list, add_criminal, criminal_details



urlpatterns = [
    
    path('',views.index,name="index"),
    path('register/',views.register, name='register'),
    path('user_landing/', user_landing, name='user_landing'),
    path('dashboard/',admindashboard,name="dashboard"),
    path('user_account/',user_account,name='user_account'),
    path("file_complaint", file_complaint, name='file_complaint'), 
    path('logout_view/', logout_view, name='logout_view'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('generate_pdf/<int:complaint_id>/', generate_pdf, name='generate_pdf'),
    path('view_user_complaints/', view_user_complaints, name='view_user_complaints'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
     path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_thankyou/', views.feedback_thankyou, name='feedback_thankyou'), 
    path("adminfeedback",views.adminfeedback,name='adminfeedback'),
     path('most_wanted_list/', most_wanted_list, name='most_wanted_list'),
    path('add_criminal/', add_criminal, name='add_criminal'),
    path('criminal_details/<int:criminal_id>/', criminal_details, name='criminal_details'),
    path('missing_persons/', missing_person_list, name='missing_person_list'),
    path('missing_personsa/', missing_person_lista, name='missing_person_lista'),
    path('missing_person_details/<int:missing_person_id>/', missing_person_details, name='missing_person_details'),
    path('report_missing_person/', report_missing_person, name='report_missing_person'),
    path('police_station_registration/', views.police_station_registration, name='police_station_registration'),
    path('police_home/', views.police_home, name='police_home')
]
