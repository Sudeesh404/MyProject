from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import ComplaintForm
from .models import Complaint 
from .models import UserProfile
from .models import Feedback
from .forms import UserProfileForm,CustomUserChangeForm
from .forms import RegistrationForm
from .models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login')  # Redirect to a success page

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
# Create your views here.


def index(request):
    
    return render(request,'index.html')
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check for predefined admin credentials
            if username == 'admin' and password == 'admin':
                #login(request, user)
                return redirect('dashboard')  # Redirect to the admin dashboard
            else:
                login(request, user)
                return redirect('user_landing')  # Redirect to the user landing page for regular users
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    
    return render(request, 'login.html')

@login_required
@never_cache
def user_landing(request):
    # Your view logic goes here
    return render(request, 'user_landing.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('update_profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})

@login_required
@never_cache
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

@login_required
@never_cache
def view_user_complaints(request):
    user_complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'user_complaints.html', {'user_complaints': user_complaints})


def admindashboard(request):
    context = {
        # Add context data here
    }
    return render(request, 'admin/dashboard.html', context)


def user_account(request):
    role_filter = request.GET.get('role')
    users = User.objects.filter(~Q(is_superuser=True))  # Exclude superusers by default

    if role_filter:
        users = users.filter(role=role_filter)

    context = {'User_profiles': users, 'role_filter': role_filter}
    return render(request, 'admin/user_account.html',context)


def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('admin/activation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'isushi2023x@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/user_account/')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivate the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('admin/deactivation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'isushi2023x@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/user_account/')

def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin/complaint_list.html', {'complaints': complaints})

def generate_pdf(request, complaint_id):
    # Get the complaint_instance based on complaint_id
    complaint_instance = get_object_or_404(Complaint, id=complaint_id)

    now = timezone.now()
    # Context for the template
    context = {'complaint_instance': complaint_instance,'now': now}
    # Render the template
    template = get_template('generate_pdf.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=complaint_{complaint_instance.id}.pdf'

    # Generate PDF using xhtml2pdf library
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response


@never_cache
@login_required(login_url="login")
def submit_feedback(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        if feedback_message:
            Feedback.objects.create(user=request.user, message=feedback_message)
            # You can add additional logic here (e.g., sending a confirmation email)
            return redirect('feedback_thankyou')

    return render(request, 'admin/feedback_form.html')


def feedback_thankyou(request):
     return render(request,'admin/feedback_thankyou.html')


from django.shortcuts import render
from .models import Feedback

def adminfeedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'admin/adminfeedback.html', {'feedback_list': feedback_list})


def logout_view(request):
    request.session.flush() 
    return redirect('login')  

# def logout_view(request):
#     logout(request)
#     return redirect('login')

from .models import Criminal
from .forms import CriminalForm

def most_wanted_list(request):
    criminals = Criminal.objects.all()
    return render(request, 'most_wanted_list.html', {'criminals': criminals})

def add_criminal(request):
    if request.method == 'POST':
        form = CriminalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('most_wanted_list')
    else:
        form = CriminalForm()

    return render(request, 'add_criminal.html', {'form': form})

def criminal_details(request, criminal_id):
    criminal = Criminal.objects.get(pk=criminal_id)
    return render(request, 'criminal_details.html', {'criminal': criminal})