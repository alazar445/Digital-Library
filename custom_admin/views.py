from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'custom_admin/admin_panel.html')


def custom_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # checks if the user is staff
                login(request, user)
                print(request.user.is_authenticated)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You are not authorized to access this page.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'custom_admin/login.html')


def custom_logout(request):
    logout(request)
    print(request.user.is_authenticated)
    return redirect('admin_login')

from .forms import BookForm

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard') 
        
    else:
        form = BookForm()
    return render(request, 'custom_admin/add_book.html', {'form': form})
