from .models import Record

# Create sign up form
# This form is used to register new users
# It inherits from UserCreationForm, which is a built-in form for user registration
# It adds fields for first name and last name
# It also customizes the appearance of the form fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create sign up form
class SignUpForm(UserCreationForm):
    # Define form fields
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    # Define model and fields
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # Define form initialization
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Add custom styling to the username field, password1 field, and password2 field
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
            self.fields[field_name].label = ''

        # Add custom styling and help text to the password1 field
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small"><li>Your password can\'t be too similar '
            'to your other personal information.</li><li>Your password must contain at least '
            '8 characters.</li><li>Your password can\'t be a commonly used '
            'password.</li><li>Your password can\'t be entirely numeric.</li></ul>')

        # Add custom styling and help text to the password2 field
        self.fields['password2'].help_text = (
            '<span class="form-text text-muted"><small>Enter the same password as before, '
            'for verification.</small></span>')

    # Define form validation
    def clean_username(self):
        # Check if the username already exists
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        # Check if the email already exists
        email = self.cleaned_data['email']
        return email

    def clean(self):
        # Check if the passwords match
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data


# Create custom date time input
# This class is used to customize the appearance of the date time input field
# It inherits from forms.DateTimeInput, which is a built-in form field for date time input
# It sets the input type to 'datetime-local' to display a date time picker in the browser
# It also customizes the appearance of the form field
class CustomDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


# Define choices for contact status
contact_status_choices = [
    ('', 'Select an option'),
    ('Contact successful', 'Contact successful'),
    ('Awaiting response', 'Awaiting response'),
    ('No contact possible', 'No contact possible'),
]


# Create add record form
# This form is used to add new payment records
# It inherits from forms.ModelForm, which is a built-in form for model-based forms
# It adds fields for payment reference, first name, last name, contact method, contact date, contact status, and notes
class AddRecordForm(forms.ModelForm):
    # Define form fields
    payment_reference = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Payment Reference'}))
    first_name = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    contact_method = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Contact Method'}))
    contact_date = forms.DateTimeField(required=True, label="",
                                       widget=CustomDateTimeInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Contact Date'})
                                       )
    contact_status = forms.ChoiceField(choices=contact_status_choices, required=True, label="", widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Contact Status'}))
    notes = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Notes'}))

    # Define model and fields
    class Meta:
        model = Record
        fields = ('payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status',
                  'notes')


# Create update record form
# This form is used to update existing payment records
# It inherits from forms.ModelForm, which is a built-in form for model-based forms
# It adds fields for payment reference, first name, last name,
# contact method, contact date, contact status, notes, and updated by
class UpdateRecordForm(forms.ModelForm):
    # Define form fields
    payment_reference = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Payment Reference'}))
    first_name = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    contact_method = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Contact Method'}))
    contact_date = forms.DateTimeField(required=True, label="",
                                       widget=CustomDateTimeInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Contact Date'})
                                       )
    contact_status = forms.ChoiceField(choices=contact_status_choices, required=True, label="", widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Contact Status'}))
    notes = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Notes'}))
    updated_by = forms.CharField(required=True, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Updated by:'}))

    # Define model and fields
    class Meta:
        model = Record
        fields = ('payment_reference', 'first_name', 'last_name', 'contact_method', 'contact_date', 'contact_status',
                  'notes', 'updated_by')


# Create record search form
# This form is used to search for payment records
# It adds a field for the search term
# It also customizes the appearance of the form field
class RecordSearch(forms.Form):
    # Define form fields
    search = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search...'}))
