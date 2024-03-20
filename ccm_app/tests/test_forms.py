from django.test import TestCase
from ccm_app.forms import SignUpForm, AddRecordForm, UpdateRecordForm, RecordSearch
from django.contrib.auth.models import User

# This test case is used to test the SignUpForm
class SignUpFormTest(TestCase):
    # This test is used to check if the form has the correct fields
    def test_form_has_fields(self):
        form = SignUpForm()
        expected_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # This test is used to check if the form is valid
    def test_form_valid(self):
        form = SignUpForm(data={
            'username': 'test_user',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123.',
            'password2': 'password123.'
        })
        self.assertTrue(form.is_valid())

    # This test is used to check if the form is invalid
    def test_form_invalid(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    # This test is used to check if the form is invalid when the password is too short
    def test_clean_email(self):
        form = SignUpForm(data={
            'username': 'test_user',
            'email': '',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])
        
    # This test is used to check if the form is invalid when the username is empty
    def test_clean_username(self):
        form = SignUpForm(data={
            'username': '',
            'email': 'user_o@he.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        
    # This test is used to check if the form is invalid when the username already exists
    def test_username_already_exists(self):
        user = User.objects.create(username='test_user', password='password123')
        form = SignUpForm(data={
            'username': 'test_user',
            'email': '',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Username already exists.'])

# This test case is used to test the AddRecordForm
class AddRecordFormTest(TestCase):
    # This test is used to check if the form has the correct fields
    def test_form_has_fields(self):
        form = AddRecordForm()
        expected_fields = ['payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status', 'notes']
        self.assertTrue(all(field in form.fields for field in expected_fields))

# This test case is used to test the UpdateRecordForm
class UpdateRecordFormTest(TestCase):
    # This test is used to check if the form has the correct fields
    def test_form_has_fields(self):
        form = UpdateRecordForm()
        expected_fields = ['payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status', 'notes', 'updated_by']
        self.assertTrue(all(field in form.fields for field in expected_fields))

#   This test case is used to test the RecordSearch
class RecordSearchTest(TestCase):
    # This test is used to check if the form has the correct fields
    def test_form_field(self):
        form = RecordSearch()
        expected_fields = ['search']
        self.assertTrue(all(field in form.fields for field in expected_fields))
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # Test the form's search functionality if applicable.
