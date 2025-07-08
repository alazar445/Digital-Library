from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    pdf_file = models.FileField(upload_to='books/pdfs/', null=True, blank=True)

    def __str__(self):
        return self.title
