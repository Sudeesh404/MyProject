from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import ComplaintForm
from .models import Complaint 
# from .models import UserProfile
# from .forms import UserProfileForm,CustomUserChangeForm
from .forms import RegistrationForm


# Create your views here.
def index(request):
    
    return render(request,'index.html')
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user_landing')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user but don't save it yet
            user = form.save(commit=False)

            # Additional data
            user.Name = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.mobile=form.cleaned_data['mobile']
            user.address=form.cleaned_data['address']
            entered_password = form.cleaned_data['password1']
            user.set_password(entered_password)
           
            # Save the user and set a hashed password
            user.save()
            
    
            # Log in the user
            login(request, user)

            return redirect('login')  # Redirect to the home page or any other desired page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def user_landing(request):
    # Your view logic goes here
    return render(request, 'user_landing.html')

@login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('update_profile')
#     else:
#         form = UserProfileForm(instance=request.user)

#     return render(request, 'update_profile.html', {'form': form})

def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return render(request, 'user_landing.html')  # Create success.html for a success message
    else:
        form = ComplaintForm()

    return render(request, 'file_complaint.html', {'form': form})

def view_user_complaints(request):
    user_complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'user_complaints.html', {'user_complaints': user_complaints})



# def update_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
#     if request.method == 'POST':
#         user_form = CustomUserChangeForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, instance=user_profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile_updated')  # Redirect to a success page
#     else:
#         user_form = CustomUserChangeForm(instance=request.user)
#         profile_form = UserProfileForm(instance=user_profile)

#     return render(request, 'user/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def logout_view(request):
    request.session.flush() 
    return redirect('login')  
