from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ccm_app.models import Record
from ccm_app.forms import SignUpForm


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ccm_app.models import Record
from ccm_app.forms import SignUpForm

#This test case is used to test the views
class ViewTestCase(TestCase):
    # This method is used to set up the test
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.record = Record.objects.create(
            created_by=self.user,
            payment_reference='REF123',
            first_name='John',
            last_name='Doe',
            contact_method='Email',
            contact_date='2024-03-06 12:00',
            contact_status='Contact successful',
            notes='Test note',
        )
        self.client = Client()

    # Home View Tests
    # Verify that the home page is accessible without login
    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # Verify that authenticated users can access the home page and see their records
    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue('records' in response.context)
        self.assertEqual(list(response.context['records']), [self.record])

    # Attempt to log in with wrong credentials and ensure redirection to the home page for retry
    def test_home_view_error_message(self):
        response = self.client.post(reverse('home'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    # Register View Tests
    # Ensure the registration form is presented to unauthenticated users
    def test_register_user_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    # Confirm that a new user can successfully register with valid data
    def test_register_user_view_post_valid(self):
        user_count = User.objects.count()
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertRedirects(response, reverse('home'))

    # Test that the registration process fails with invalid data and errors are displayed
    def test_register_user_view_post_invalid(self):
        user_count = User.objects.count()
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': '',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
        self.assertTrue(response.context['form'].errors)

    # Login and Logout View Tests
    # Test the login process for a user with correct credentials and subsequent logout
    def test_login_logout_flow(self):
        # Login
        login_response = self.client.post(reverse('home'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(login_response, reverse('home'))

        # Logout
        logout_response = self.client.get(reverse('logout'))
        self.assertRedirects(logout_response, reverse('home'))

    # Record View Tests
    # Confirm that authenticated users can view individual record details
    def test_payment_record_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('record', args=[self.record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        self.assertEqual(response.context['record'], self.record)

    # Ensure that attempting to view a record without being logged in redirects to the home page
    def test_payment_record_view_unauthenticated(self):
        response = self.client.get(reverse('record', args=[self.record.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Add Record View Tests
    # Check that authenticated users can access the form to add a new record
    def test_add_record_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_record.html')
        self.assertTrue('form' in response.context)
        self.assertEqual(response.context['form']._meta.model, Record)

    # Verify redirection to the home page when unauthenticated users attempt to access the add record form
    def test_add_record_view_unauthenticated(self):
        response = self.client.get(reverse('add_record'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Confirm that submitting a valid new record form by an authenticated user adds the record
    def test_add_record_view_post_valid(self):
        record_count = Record.objects.count()
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_record'), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': 'Test note',
        })
        self.assertEqual(Record.objects.count(), record_count + 1)
        self.assertRedirects(response, reverse('home'))

    # Ensure that an invalid form submission for adding a record shows errors without adding the record
    def test_add_record_view_post_invalid(self):
        record_count = Record.objects.count()
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_record'), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': '',
        })
        self.assertEqual(Record.objects.count(), record_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_record.html')
        self.assertTrue(response.context['form'].errors)

    # Check if the add record view is accessible to unauthenticated users
    def test_add_record_view_post_unauthenticated(self):
        record_count = Record.objects.count()
        response = self.client.post(reverse('add_record'), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': 'Test note',
        })
        self.assertEqual(Record.objects.count(), record_count)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Update Record View Tests
    # Test that authenticated users can access the update form for an existing record
    def test_update_record_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('update_record', args=[self.record.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_record.html')
        self.assertTrue('form' in response.context)
        self.assertEqual(response.context['form']._meta.model, Record)

    # Verify that unauthenticated users are redirected when attempting to access the update record form
    def test_update_record_view_unauthenticated(self):
        response = self.client.get(reverse('update_record', args=[self.record.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Confirm that an authenticated user can successfully update a record with valid data
    def test_update_record_view_post_valid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_record', args=[self.record.id]), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': 'Test note',
            'updated_by': 'John Doe',
        })
        self.record.refresh_from_db()
        self.assertEqual(self.record.payment_reference, 'REF456')
        self.assertEqual(self.record.first_name, 'Jane')
        self.assertEqual(self.record.last_name, 'Doe')
        self.assertEqual(self.record.contact_method, 'Phone')
        self.assertEqual(self.record.contact_status, 'Contact successful')
        self.assertEqual(self.record.notes, 'Test note')
        self.assertEqual(self.record.updated_by, 'John Doe')
        self.assertRedirects(response, reverse('home'))

    # Test that submitting invalid update data does not update the record and shows errors
    def test_update_record_view_post_invalid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_record', args=[self.record.id]), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': '',
            'updated_by': 'John Doe',
        })
        self.record.refresh_from_db()
        self.assertEqual(self.record.payment_reference, 'REF123')
        self.assertEqual(self.record.first_name, 'John')
        self.assertEqual(self.record.last_name, 'Doe')
        self.assertEqual(self.record.contact_method, 'Email')
        self.assertEqual(self.record.contact_status, 'Contact successful')
        self.assertEqual(self.record.notes, 'Test note')
        self.assertIsNone(self.record.updated_by)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_record.html')
        self.assertTrue(response.context['form'].errors)

    # Verify the behaviour of an unauthenticated POST request to the update record view
    def test_update_record_view_post_unauthenticated(self):
        response = self.client.post(reverse('update_record', args=[self.record.id]), {
            'payment_reference': 'REF456',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'contact_method': 'Phone',
            'contact_date': '2024-03-06T12:00',
            'contact_status': 'Contact successful',
            'notes': 'Test note',
            'updated_by': 'John Doe',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Delete Record View Tests
    # Confirm that authenticated users can delete a record and are redirected to the home page
    def test_delete_record_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        expected_redirect_url = reverse('home')
        response = self.client.get(reverse('delete_record', args=[self.record.id]))
        self.assertRedirects(response, expected_redirect_url)

    # Ensure that unauthenticated users cannot access the delete functionality and are redirected
    def test_delete_record_view_unauthenticated(self):
        response = self.client.get(reverse('delete_record', args=[self.record.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Verify that attempting to delete a record without authentication does not change the record count
    def test_delete_record_view_post_unauthenticated(self):
        record_count = Record.objects.count()
        response = self.client.post(reverse('delete_record', args=[self.record.id]))
        self.assertEqual(Record.objects.count(), record_count)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Confirm that staff users can delete a record, decreasing the total count of records
    def test_delete_record_view_post_staff(self):
        self.user.is_staff = True
        self.user.save()
        record_count = Record.objects.count()
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_record', args=[self.record.id]))
        self.assertEqual(Record.objects.count(), record_count - 1)
        self.assertRedirects(response, reverse('home'))

    # User Management View Tests
    # Verify staff user access to the user management view with user listings
    def test_user_management_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_management'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the user management view is accessible to unauthenticated users
    def test_user_management_view_unauthenticated(self):
        response = self.client.get(reverse('user_management'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

 # Check if the user management view is accessible to staff users
    def test_user_management_view_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management.html')
        self.assertTrue('users' in response.context)
        self.assertEqual(list(response.context['users']), [self.user])

    # Search Results View Tests
    # Test that submitting a search query as a staff user displays relevant search results
    def test_search_results_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('search_results'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the search results view is accessible to unauthenticated users
    def test_search_results_view_unauthenticated(self):
        response = self.client.get(reverse('search_results'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the search results view is accessible to staff users
    def test_search_results_view_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('search_results'),
                                    {'searched': 'John'})
        self.assertTemplateUsed(response, 'search_results.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn('records', response.context)
        self.assertIn('searched', response.context)
        self.assertEqual(response.context['searched'], 'John')

    # Check if the search results view is accessible to staff users via POST request
    def test_search_results_view_post_unauthenticated(self):
        response = self.client.post(reverse('search_results'), {'search': 'John'})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Audit Logs View Tests
    # Confirm that staff users can access audit logs to review changes and actions logged by the system
    def test_audit_logs_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('audit_logs'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the audit logs view is accessible to unauthenticated users
    def test_audit_logs_view_unauthenticated(self):
        response = self.client.get(reverse('audit_logs'))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the audit logs view is accessible to staff users
    def test_audit_logs_view_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit_logs.html')
        self.assertTrue('records' in response.context)
        self.assertEqual(list(response.context['records']), [self.record])

    # User Active Status View Tests

    # Verify that staff users can toggle the active status of a user account through a POST request
    def test_user_active_status_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to unauthenticated users
    def test_user_active_status_view_unauthenticated(self):
        response = self.client.get(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to staff users
    def test_user_active_status_view_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('user_management'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to staff users via POST request
    def test_user_active_status_view_post_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('user_management'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to authenticated staff users via POST request
    def test_user_active_status_view_post_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to unauthenticated users via POST request
    def test_user_active_status_view_post_unauthenticated(self):
        response = self.client.post(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

    # Check if the user active status view is accessible to staff users via POST request
    def test_user_active_status_view_post_staff_superuser(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post(reverse('user_active_status', args=[self.user.id]))
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)




