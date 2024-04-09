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
#mainproject
from .forms import PoliceStationRegistrationForm
from .models import BlogPost

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
            login(request, user)
            if user.role == user.Role.OFFICER:  # Accessing role through instance
                return redirect('police_home')  # Redirect to the police home page
            elif username == 'admin' and password == 'admin':
                return redirect('dashboard')
            else:
                return redirect('user_landing')
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
    return redirect('index')  

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

    return render(request, 'admin/add_criminal.html', {'form': form})

def criminal_details(request, criminal_id):
    criminal = Criminal.objects.get(pk=criminal_id)
    return render(request, 'criminal_details.html', {'criminal': criminal})

# views.py
from django.shortcuts import render, redirect
from .models import MissingPerson
from .forms import MissingPersonForm

def missing_person_list(request):
    missing_persons = MissingPerson.objects.all()
    return render(request, 'missing_person_list.html', {'missing_persons': missing_persons})

def report_missing_person(request):
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_landing')
    else:
        form = MissingPersonForm()

    return render(request, 'report_missing_person.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from .models import MissingPerson

def missing_person_details(request, missing_person_id):
    missing_person = get_object_or_404(MissingPerson, id=missing_person_id)
    
    if request.method == 'POST':
        # Retrieve the selected status from the form data
        status = request.POST.get('status')
        
        # Update the status of the missing person object
        missing_person.status = status
        
        # Save the changes to the database
        missing_person.save()
        
        # Redirect to the same page to prevent form resubmission
        return redirect('missing_person_details', missing_person_id=missing_person_id)
    
    # If the request method is GET, render the template with the missing person details
    return render(request, 'admin/missing_person_details.html', {'missing_person': missing_person})


from .forms import UpdateStatusForm
def missing_person_lista(request):
    missing_persons = MissingPerson.objects.all()

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            # Retrieve the MissingPerson instance
            missing_person_id = form.cleaned_data['missing_person']
            missing_person = MissingPerson.objects.get(id=missing_person_id)

            # Update the status
            missing_person.status = form.cleaned_data['status']
            missing_person.save()

            # Redirect to the same page after updating the status
            return redirect('missing_person_lista')

    # If it's a GET request or the form is not valid, render the template with the form
    form = UpdateStatusForm()
    return render(request, 'admin/missing_person_lista.html', {'missing_personsa': missing_persons, 'form': form})

#mainproject
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from .forms import PoliceStationRegistrationForm

def police_station_registration(request):
    if request.method == 'POST':
        form = PoliceStationRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to a success page
    else:
        form = PoliceStationRegistrationForm()
    return render(request, 'police_station_registration.html', {'form': form})

def police_home(request):
    # Add logic here if needed
    return render(request, 'police_home.html')




from .forms import BlogPostForm
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.admin = request.user
            blog_post.save()
            return redirect('/add')  # Redirect to the blog post list page
    else:
        form = BlogPostForm()

    return render(request, 'admin/add_blog_post.html', {'form': form})


@never_cache
@login_required(login_url="/auth_app/handlelogin/")
def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    top_three_posts = BlogPost.objects.order_by('-views')[:3]
    return render(request, 'customer/blog_post_list.html', {'blog_posts': blog_posts,'top_three_posts':top_three_posts})

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})