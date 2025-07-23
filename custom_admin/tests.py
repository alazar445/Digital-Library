# ------------------- UNIT TESTS -------------------
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book
from .forms import BookForm
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class BookModelUnitTest(TestCase):
    def test_str_method(self):
        book = Book(title='UnitTest Book', author='Author', publication_date='2024-01-01', isbn='1111111111111', genre='Test', language='EN')
        self.assertEqual(str(book), 'UnitTest Book')

class BookFormUnitTest(TestCase):
    def test_valid_form(self):
        data = {
            'title': 'FormTest Book',
            'author': 'Author',
            'publication_date': '2024-01-01',
            'isbn': '2222222222222',
            'genre': 'Test',
            'language': 'EN',
        }
        form = BookForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'title': '',  # Missing title
            'author': 'Author',
            'publication_date': '2024-01-01',
            'isbn': '2222222222222',
            'genre': 'Test',
            'language': 'EN',
        }
        form = BookForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

# ------------------- INTEGRATION TESTS -------------------

class CustomAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.normal_user = User.objects.create_user(username='user', password='userpass', is_staff=False)

    def test_admin_login_success(self):
        response = self.client.post(reverse('admin_login'), {'username': 'admin', 'password': 'adminpass'})
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_admin_login_failure(self):
        response = self.client.post(reverse('admin_login'), {'username': 'admin', 'password': 'wrongpass'})
        self.assertContains(response, 'Invalid username or password', status_code=200)

    def test_non_staff_login(self):
        response = self.client.post(reverse('admin_login'), {'username': 'user', 'password': 'userpass'})
        self.assertContains(response, 'You are not authorized to access this page.', status_code=200)

    def test_dashboard_requires_admin(self):
        # Not logged in
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)
        # Logged in as normal user
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)
        # Logged in as admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome admin')

    def test_logout(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('admin_login'))

    def test_add_book_view_requires_admin(self):
        # Not logged in
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 403)
        # Logged in as normal user
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 403)
        # Logged in as admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Book')

    def test_add_book_form(self):
        self.client.login(username='admin', password='adminpass')
        pdf_file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'publication_date': '2024-01-01',
            'isbn': '1234567890123',
            'genre': 'Fiction',
            'language': 'English',
            'pdf_file': pdf_file,
        }
        response = self.client.post(reverse('add_book'), data, follow=True)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.assertTrue(Book.objects.filter(title='Test Book').exists())

    def test_add_book_form_invalid(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'title': '',  # Missing required field
            'author': 'Author Name',
            'publication_date': '2024-01-01',
            'isbn': '1234567890123',
            'genre': 'Fiction',
            'language': 'English',
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    # ------------------- UNIT TESTS FOR DISPLAY BOOKS VIEW -------------------
    def test_display_books_requires_admin(self):
        # Not logged in
        response = self.client.get(reverse('display_books'))
        self.assertEqual(response.status_code, 403)
        # Logged in as normal user
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('display_books'))
        self.assertEqual(response.status_code, 403)
        # Logged in as admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('display_books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Books')

    def test_display_books_shows_books(self):
        self.client.login(username='admin', password='adminpass')
        Book.objects.create(
            title='Book 1', author='Author 1', publication_date='2024-01-01',
            isbn='1111111111111', genre='Genre1', language='EN'
        )
        Book.objects.create(
            title='Book 2', author='Author 2', publication_date='2024-01-02',
            isbn='2222222222222', genre='Genre2', language='FR'
        )
        response = self.client.get(reverse('display_books'))
        self.assertContains(response, 'Book 1')
        self.assertContains(response, 'Book 2')
        self.assertContains(response, 'Author 1')
        self.assertContains(response, 'Author 2')
        self.assertContains(response, 'Genre1')
        self.assertContains(response, 'Genre2')

    # ------------------- INTEGRATION TESTS FOR DISPLAY BOOKS VIEW -------------------
    def test_display_books_integration_admin_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('display_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_admin/display_books.html')
        self.assertContains(response, 'Books')

    def test_display_books_integration_shows_multiple_books(self):
        self.client.login(username='admin', password='adminpass')
        Book.objects.create(
            title='Integration Book 1', author='Int Author 1', publication_date='2024-01-01',
            isbn='3333333333333', genre='IntGenre1', language='EN'
        )
        Book.objects.create(
            title='Integration Book 2', author='Int Author 2', publication_date='2024-01-02',
            isbn='4444444444444', genre='IntGenre2', language='FR'
        )
        response = self.client.get(reverse('display_books'))
        self.assertContains(response, 'Integration Book 1')
        self.assertContains(response, 'Integration Book 2')
        self.assertContains(response, 'Int Author 1')
        self.assertContains(response, 'Int Author 2')
        self.assertContains(response, 'IntGenre1')
        self.assertContains(response, 'IntGenre2')

    def test_display_books_integration_no_books(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('display_books'))
        self.assertContains(response, 'No books found.')
