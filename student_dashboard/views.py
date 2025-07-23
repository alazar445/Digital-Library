from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'student_dashboard/dashboard.html')
