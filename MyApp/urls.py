from django.contrib import admin
from django.urls import path
from MyApp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from .views import logout_view
from .views import user_landing
# from .views import update_profile
from .views import view_user_complaints
from .views import file_complaint

urlpatterns = [
    
    path('',views.index,name="index"),
    path('register/',views.register, name='register'),
    path('user_landing/', user_landing, name='user_landing'),
    path("file_complaint", file_complaint, name='file_complaint'), 
    path('logout/', logout_view, name='logout'),
    path('view_user_complaints/', view_user_complaints, name='view_user_complaints'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
