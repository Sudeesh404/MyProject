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


urlpatterns = [
    
    path('',views.index,name="index"),
    path('register/',views.register, name='register'),
    path('user_landing/', user_landing, name='user_landing'),
    path("dashboard/",admindashboard,name="dashboard"),
    path('user_account',user_account,name='user_account'),
    path("file_complaint", file_complaint, name='file_complaint'), 
    path('logout/', logout_view, name='logout'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('view_user_complaints/', view_user_complaints, name='view_user_complaints'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
]
