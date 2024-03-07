from ccm_app.models import Record
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

class RecordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified data for all class methods
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_record_creation(self):
        # Test creating a new Record instance
        record = Record.objects.create(
            created_by=self.user,
            payment_reference='ABC123',
            first_name='John',
            last_name='Doe',
            contact_method='Email',
            contact_date=timezone.now(),
            contact_status='Pending',
            notes='Initial contact made.',
            updated_by='Jane Doe',
        )
        # Assert the record was created correctly
        self.assertTrue(isinstance(record, Record))
        self.assertEqual(record.created_by, self.user)
        self.assertEqual(record.payment_reference, 'ABC123')
        self.assertEqual(record.first_name, 'John')
        self.assertEqual(record.last_name, 'Doe')
        self.assertEqual(record.contact_method, 'Email')
        self.assertEqual(record.contact_status, 'Pending')
        self.assertEqual(record.notes, 'Initial contact made.')
        self.assertEqual(record.updated_by, 'Jane Doe')

    def test_record_fields_nullable(self):
        # Test creating a Record with minimal required fields to ensure null=True fields can be left blank
        record = Record.objects.create(
            created_by=self.user,
            payment_reference='XYZ789',
            first_name='Alice',
            last_name='Smith',
            contact_method='Phone',
            contact_date=timezone.now(),
            contact_status='Completed',
            notes='',
        )
        # Verify that the created record can be saved with null fields where allowed
        self.assertTrue(isinstance(record, Record))
        self.assertIsNone(record.updated_by)