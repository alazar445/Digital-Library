from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.http import HttpResponseForbidden
from functools import wraps
from .models import Book
from django.db import models

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view




@admin_required
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







@admin_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard') 
        
    else:
        form = BookForm()
    return render(request, 'custom_admin/add_book.html', {'form': form})


@admin_required
def display_books(request):
    search_query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    
    return render(request, 'custom_admin/display_books.html', {'books': books, 'search_query': search_query})
