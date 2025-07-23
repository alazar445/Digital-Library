from django.shortcuts import render
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserProfile

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            education_status = form.cleaned_data['education_status']
            # Split full name for first_name, last_name
            name_parts = full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            try:
                if User.objects.filter(username=username).exists():
                    form.add_error('username', 'Username already exists.')
                elif User.objects.filter(email=email).exists():
                    form.add_error('email', 'Email already exists.')
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    # Save gender and education_status in user profile
                    UserProfile.objects.create(user=user, gender=gender, education_status=education_status)
                    return render(request, 'home/register.html', {'form': form, 'success': True})
            except IntegrityError:
                form.add_error(None, 'A server error occurred. Please try again.')
    else:
        form = RegistrationForm()
    return render(request, 'home/register.html', {'form': form})
