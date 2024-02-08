from django.db import models

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

    def __str__(self):
        return (f"{self.payment_reference} {self.first_name} {self.last_name}")