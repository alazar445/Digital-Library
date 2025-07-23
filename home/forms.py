from django import forms

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        label='Gender',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    education_status = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('researcher', 'Researcher'),
            ('other', 'Other'),
        ],
        label='Education Status',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'})) 