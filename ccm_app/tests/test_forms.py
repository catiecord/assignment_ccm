from django.test import TestCase
from ccm_app.forms import SignUpForm, AddRecordForm, UpdateRecordForm, RecordSearch
from django.contrib.auth.models import User
from ccm_app.models import Record
from django.utils import timezone

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected_fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # Add more tests to check form validation, custom behaviors, etc.

class AddRecordFormTest(TestCase):
    def test_form_has_fields(self):
        form = AddRecordForm()
        expected_fields = ['payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status', 'notes']
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # You could also test the custom validation logic, form save functionality, etc.

class UpdateRecordFormTest(TestCase):
    def test_form_has_fields(self):
        form = UpdateRecordForm()
        expected_fields = ['payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status', 'notes', 'updated_by']
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # Test updating a record, validation, and any custom methods.

class RecordSearchTest(TestCase):
    def test_form_field(self):
        form = RecordSearch()
        expected_fields = ['search']
        self.assertTrue(all(field in form.fields for field in expected_fields))

    # Test the form's search functionality if applicable.
