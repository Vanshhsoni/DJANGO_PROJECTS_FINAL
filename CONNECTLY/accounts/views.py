from django.shortcuts import render, redirect
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
# Create your views here.

# def signup(request):
#     if request.method=="POST":
#         data=request.POST
#         username=data.get("USERNAME")
#         password=data.get("PASSWORD")
#         print("USERNAME:",username)
#         print("PASSWORD :",password)
#         return HttpResponse(request,"data saved")
#     return render(request,"signups.html")

# REGISTERATION HERE
def register(request):
    if request.method == 'POST':
        # Safely access the 'username' and 'password' fields from POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another one.")
            return render(request, 'register.html')

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Log the user in after registration
            login(request, user)

            # Redirect to the main page after successful registration
            return redirect('main')  # Redirect to the main view

        except IntegrityError:
            messages.error(request, "LOGIN NOW")
            return render(request, 'login.html')

    return render(request, 'register.html')
# LOGIN HERE
def user_login(request):
    if request.method == 'POST':
        # Get username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If user is authenticated, log them in
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('/feed')  # Redirect to the main view
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')
# # OTP LOGIN
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# import random

# def Login_otp(request):
#     if request.method == "POST":
#         data = request.POST
#         email = data.get('user_email')
#         print(email)

#         otp = random.randint(100000, 999999)
        
#         # to verify otp 
#         request.session['otp'] = otp
#         request.session['email'] = email

#         # send otp using mail 
#         subject = "OTP From Django Website"
#         message = f"Your OTP is: {otp}"
#         from_email = settings.EMAIL_HOST_USER

#         send_mail(subject, message, from_email, [email])
#         # Open overlay on the front-end
#         return render(request, "login_otp.html")  # Return the same page with an overlay for OTP

#     return render(request, "login_otp.html")

# def verify_otp(request):
#     if request.method == "POST":
#         data = request.POST
#         user_otp = data.get('user_otp')

#         send_otp = request.session.get('otp')

#         if str(user_otp) == str(send_otp):
#             messages.success(request, "OTP is verified successfully")
#             return redirect('success')  # Redirect to success page after verification
#         else:
#             messages.error(request, "Invalid OTP")
            
#     return render(request, "login_otp.html")  # Return to the same page if OTP verification fails


# LOGOUT 
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('main')  # Redirect to the main page after logout