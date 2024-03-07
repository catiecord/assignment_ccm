from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, RecordSearch
from .models import Record


def home(request):
    records = Record.objects.all()
    # Check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - please try again...'))
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Don't save yet, we need to check if user is superuser
            user = form.save(commit=False)
            if form.cleaned_data['is_staff']:
                user.is_staff = True
            # Authenticate and login user
            user.set_password(form.cleaned_data['password1'])   # Set password
            user.save()
            login(request,user )
            messages.success(request, ('You have been registered! Welcome to the CCM App!'))
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def payment_record(request, pk):
    if request.user.is_authenticated:
        # Look up the payment record
        pay_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': pay_record})
    else:
        messages.success(request, 'You must be logged in to view records!')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        if request.user.is_staff:
            delete_it = Record.objects.get(id=pk)
            delete_it.delete()
            messages.success(request, 'Record has been deleted!')
            return redirect('home')
        else:
            messages.success(request, 'You must be an admin to delete records!')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to delete records!')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record has been added!')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to add records!')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record has been updated!')
                return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in to update records!')
        return redirect('home')

def user_management(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            User = get_user_model()
            users = User.objects.all()
            return render(request, 'user_management.html', {'users': users})
        else:
            messages.success(request, 'You must be an admin to view users!')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to view users!')
        return redirect('home')
def user_active_status(request, user_id):
    """
    Toggles the active status of a user account.

    - Accessible only to authenticated users due to the @login_required decorator.
    - Checks if the user is a superuser:
        - If not, the user is redirected to the home page with an error message.
    - If the user is a superuser:
        - Attempts to fetch the User object that corresponds to the provided user_id parameter.
        - If the User object is not found, an error message is displayed, and the user is redirected to the user list page.
        - If the User object is found:
            - Checks if the user to be toggled is the same as the logged-in superuser:
                - If yes, an error message is displayed, indicating that the superuser cannot deactivate their own account.
                - If no, the active status (is_active attribute) of the User object is toggled (True becomes False, and vice versa).
                - Saves the updated User object to the database.
                - Displays a success message indicating whether the account has been activated or deactivated.

    Parameters:
    - request (HttpRequest): The HTTP request object, which contains information about the current user.
    - user_id (int): The ID of the user whose active status is to be toggled.

    Returns:
    - HttpResponse: Redirects to the user list page with a success message for superusers, or to the home page with an error message for non-superusers.
    """
    User = get_user_model()
    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect("home")

    # Get the user by ID
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("user_management")

    # Check if the user to toggle is the same as the logged-in superuser
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account!")
        return redirect("user_management")

    # Toggle the user's active status
    user.is_active = not user.is_active
    user.save()

    # Provide feedback to the superuser
    if user.is_active:
        messages.success(
            request, f"{user.username}'s account has been activated."
        )
    else:
        messages.success(
            request, f"{user.username}'s account has been deactivated."
        )
    return redirect("user_management")

def search_results(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched']
            records = Record.objects.filter(
                first_name__icontains=searched) | Record.objects.filter(
                last_name__icontains=searched) | Record.objects.filter(
                payment_reference__icontains=searched)
            return render(request, 'search_results.html', {'searched': searched, 'records': records})
    else:
        messages.success(request, 'You must be logged in to search records!')
        return redirect('home')