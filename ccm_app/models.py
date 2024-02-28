from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_method = models.CharField(max_length=60)
    contact_date = models.DateTimeField()
    contact_status = models.CharField(max_length=60)
    notes = models.TextField()

class Audit(models.Model):
    """
    Represents an audit log entry to track user actions on knowledge base entries.

    Attributes:
    - user (ForeignKey): Reference to the user who performed the action.
    - action_datetime (DateTimeField): The date and time when the action was performed. Automatically set to the current date and time when a new log entry is created.
    - kb_entry (ForeignKey): Reference to the knowledge base entry that the action was performed on. Can be null if the action is not related to a specific entry.
    - action_details (CharField): A brief description of the action performed. Maximum length of 255 characters.

    The Audit model is designed to keep a log of various actions that users perform within the application,
    thereby allowing for accountability and potential analysis of user activity.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_datetime = models.DateTimeField(auto_now_add=True)
    database_entry = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True)
    action_details = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return (f"{self.payment_reference} {self.first_name} {self.last_name}")
