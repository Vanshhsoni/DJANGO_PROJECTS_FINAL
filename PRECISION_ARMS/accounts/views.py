from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your views here.
def welcome(request):
    return render(request, 'accounts/welcome.html')  # Default page if accessed via GET

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets the custom user model or default User

def register(request):
    if request.method == 'POST':
        # Retrieve fields from POST data
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        # Debugging prints
        print("Username:", username)
        print("Password:", password)
        print("Email:", email)

        # Check for empty fields and display errors
        if not username:
            messages.error(request, "Username is required.")
            return render(request, 'accounts/register.html')
        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'accounts/register.html')
        if not password:
            messages.error(request, "Password is required.")
            return render(request, 'accounts/register.html')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return render(request, 'accounts/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken. Please use another.")
            return render(request, 'accounts/register.html')

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Log in the new user after successful registration
            auth_login(request, user)
            return redirect('/armory/armory_home')  # Adjust URL as needed

        except Exception as e:
            messages.error(request, "An unexpected error occurred during registration: " + str(e))
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')


# LOGIN HERE
def login(request):
    if request.method == 'POST':
        # Get username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("username::",username)
        print("password::",password)

        #Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If user is authenticated, log them in
            auth_login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('/armory/armory_home')  # Redirect to the main view
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


# LOGOUT 
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('/')  # Redirect to the main page after logout



# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import ProfileForm
from .models import Profile

@login_required
def edit_profile(request):
    user_profile = request.user.profile  # Access the Profile related to the logged-in user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        print("Received POST request.")  # Debug line
        if form.is_valid():
            print("Form is valid.")  # Debug line
            # Save the form (profile picture)
            form.save()
            print("PROFILE PIC SAVED")
            # Update additional fields
            user_profile.address = request.POST.get('new_address', '')  # Make sure you're using 'new_address'
            user_profile.phone_number = request.POST.get('phone_number', '')
            user_profile.save()

            messages.success(request, 'Profile updated successfully.')
            print("Redirecting to profile...")  # Debug line
            return redirect(reverse('accounts:profile', args=[request.user.username]))  # Ensure the app name is 'accounts'
        else:
            print("Form is not valid:", form.errors)  # Debug line to check form errors
    else:
        form = ProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'profile/edit_profile.html', context)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    # Check if profile_picture exists, otherwise use default
    if profile.profile_picture and hasattr(profile.profile_picture, 'url'):
        profile_picture_url = profile.profile_picture.url
    else:
        profile_picture_url = static('images/default.jpg')

    context = {
        'profile_user': user,
        'user_profile': profile,
        'profile_picture': profile_picture_url,
        'address': profile.address,
        'phone_number': profile.phone_number,
    }

    return render(request, 'profile/profile.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def account_settings(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    
    return render(request, 'account_setting.html')
