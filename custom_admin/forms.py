from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'isbn', 'genre', 'language', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-input', 'form-input': 'form-input'}),
            'isbn': forms.TextInput(attrs={'class': 'form-input'}),
            'genre': forms.TextInput(attrs={'class': 'form-input'}),
            'language': forms.TextInput(attrs={'class': 'form-input'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            
        }