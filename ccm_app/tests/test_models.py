from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from ccm_app.models import Record


class RecordModelTestCase(TestCase):
    # This method is used to set up the test case
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        
    # Test record creation
    def test_record_creation(self):
        record = Record.objects.create(
            created_by=self.user,
            payment_reference='TestPayment123',
            first_name='John',
            last_name='Doe',
            contact_method='Email',
            contact_date=datetime.now(),
            contact_status='Pending',
            notes='This is a test note.',
            updated_by='Admin',
        )

        self.assertIsNotNone(record)
        self.assertEqual(record.payment_reference, 'TestPayment123')
        self.assertEqual(record.first_name, 'John')
        self.assertEqual(record.last_name, 'Doe')
        self.assertEqual(record.contact_method, 'Email')
        self.assertEqual(record.contact_status, 'Pending')
        self.assertEqual(record.notes, 'This is a test note.')
        self.assertEqual(record.updated_by, 'Admin')
        
    # Test record update
    def test_record_update(self):
        record = Record.objects.create(
            created_by=self.user,
            payment_reference='TestPayment123',
            first_name='John',
            last_name='Doe',
            contact_method='Email',
            contact_date=datetime.now(),
            contact_status='Pending',
            notes='This is a test note.',
            updated_by='Admin',
        )
        record.payment_reference = 'UpdatedPayment456'
        record.save()
        updated_record = Record.objects.get(id=record.id)
        self.assertEqual(updated_record.payment_reference, 'UpdatedPayment456')
        
    # Test record deletion
    def test_record_deletion(self):
        record = Record.objects.create(
            created_by=self.user,
            payment_reference='TestPayment123',
            first_name='John',
            last_name='Doe',
            contact_method='Email',
            contact_date=datetime.now(),
            contact_status='Pending',
            notes='This is a test note.',
            updated_by='Admin',
        )
        record.delete()
        with self.assertRaises(Record.DoesNotExist):
            Record.objects.get(id=record.id)

