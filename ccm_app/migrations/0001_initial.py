# Generated by Django 5.0.1 on 2024-02-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_reference', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact_method', models.CharField(max_length=60)),
                ('contact_date', models.DateTimeField()),
                ('contact_status', models.CharField(max_length=60)),
                ('notes', models.TextField()),
            ],
        ),
    ]