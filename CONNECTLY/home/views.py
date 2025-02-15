from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("WELCOME TO HOME PAGE")

# def homepage(request):
#     return render(request,"index.html")
    
from django.shortcuts import render

from django.shortcuts import render

def load_main(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # Get the value of the clicked button

        if action == 'register':
            return render(request, 'register.html')  # Render register page
        elif action == 'login':
            return render(request, 'login.html')  # Render login page
    return render(request, 'show_main.html')  # Default page if accessed via GET

def send_email_view(request):
    if request.method == "POST":
        data = request.POST
        client_mail = data.get('client_mail')
        content_mail = data.get('content_mail')
        print(content_mail)
        print(client_mail)

        sender_name = "Your Name"  # You can customize this
        sender_email = client_mail
        subject = "Your Subject Here"  # You can set this as a custom subject
        message = content_mail

        # Send the email using Django's send_mail function
        send_mail(
            subject,  # Subject of the email
            message,  # Message content
            "sonivanshmaster@gmail.com",  # From email
            [sender_email],  # To email (recipient)
            fail_silently=False,  # To raise errors if sending fails
        )  
    return render(request, "send_email.html")

# def Login_otp(request):
#     if request.method == "POST":
#         data = request.POST
#         email = data.get('email')
#         print(email)

#         otp = random.randint(100000,999999)
        

#         # to verify otp 
#         request.session['otp'] = otp
#         request.session['email'] = email



#         # send otp using mail 
#         subject = "OTP From django website"
#         message = f"Your otp is here :-> {otp}"
#         from_email = settings.EMAIL_HOST_USER

#         send_mail(subject,message,from_email,[email])
#         return redirect('verify_otp')
    
#     return render(request,"login_otp.html")


# def verify_otp(request):
#     if request.method == "POST":
#         data = request.POST
#         user_otp = data.get('user_otp')

#         send_otp = request.session.get('otp')


#         if str(user_otp)==str(send_otp):
#             messages.success(request,"otp is Verified sucessfully")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid Otp")
            
#     return render(request,"verify_otp.html")

