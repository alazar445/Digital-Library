from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    education_status = models.CharField(max_length=20, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('researcher', 'Researcher'), ('other', 'Other')])

    def __str__(self):
        return self.user.username
