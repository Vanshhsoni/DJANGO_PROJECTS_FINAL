import os
import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import User, UserQuestionnaire



otp_store = {}
User = get_user_model()

def load_signup(request):
    return render(request, 'accounts/signup.html')

def load_login(request):
    return render(request, 'accounts/login.html')

def login_signup(request):
    return render(request,'accounts/login_signup.html')
@login_required
def x(request):
    return render(request, 'accounts/x.html')  # Dummy success/dashboard page

@login_required
def z(request):
    return render(request,'accounts/z.html')



def signup_access(request):
    if request.method == 'POST':
        data = request.POST
        profile_picture = request.FILES.get('profile_picture')

        email = data.get('college_email')
        if not email.endswith('@poornima.org'):
            messages.error(request, "Use only your college email (@poornima.org).")
            return redirect('accounts:load_signup')

        if User.objects.filter(username=data['username']).exists():
            messages.error(request, 'Username already taken.')
            return redirect('accounts:load_signup')

        if User.objects.filter(college_email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('accounts:load_signup')

        if data['password'] != data['confirm_password']:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:load_signup')

        # Use create_user to handle password hashing
        user = User.objects.create_user(
            full_name=data['full_name'],
            college_email=email,
            username=data['username'],
            password=data['password'],  # Hashed automatically
            dob=data['dob'],
            college=data['college'],
            department=data['department'],
            gender=data['gender'],
            bio=data['bio']
        )

        if profile_picture:
            path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', user.username)
            os.makedirs(path, exist_ok=True)
            fs = FileSystemStorage(location=path)
            filename = fs.save(profile_picture.name, profile_picture)
            user.profile_picture.name = f'profile_pics/{user.username}/{filename}'
            user.save()

        messages.success(request, "Account created! Now login with OTP.")
        return redirect('accounts:load_login')

    return render(request, 'accounts/signup.html')


def login_access(request):
    if request.method == 'POST':
        email = request.POST.get('college_email')
        try:
            user = User.objects.get(college_email=email)
            otp = str(random.randint(100000, 999999))
            otp_store[email] = otp

            send_mail(
                subject="Your PoornimaX OTP",
                message=f"Your OTP is: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )

            return render(request, 'accounts/login.html', {
                'show_otp': True,
                'email': email
            })

        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('accounts:load_login')

    return render(request, 'accounts/login.html')


def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('college_email')
        otp = request.POST.get('otp')

        if otp_store.get(email) == otp:
            try:
                user = User.objects.get(college_email=email)
                user.otp_verified = True
                user.save()

                login(request, user)
                print("LOGGED IN")  # 🔑 THIS is what logs user in properly
                if user.has_answered_questionnaire:
                    return redirect('feed:home')  # Redirect to the page if the user has already answered the questionnaire
                else:
                    return redirect('accounts:x')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid OTP.")

    return redirect('accounts:load_login')


@login_required
def answers_view(request):
    user = request.user
    questionnaire = UserQuestionnaire.objects.get(user=user)

    def to_list(value):
        return [v.strip() for v in value.split(',')] if value else []

    context = {
        'user': user,
        'questionnaire': questionnaire,
        'hobbies': to_list(questionnaire.hobbies),
        'college_events': to_list(questionnaire.college_events),
        'weekend_plans': to_list(questionnaire.weekend_plans),
        'friendship_values': to_list(questionnaire.friendship_values),
        'content_posting': to_list(questionnaire.content_posting),
        'college_excitements': to_list(questionnaire.college_excitements),
        'learning_preferences': to_list(questionnaire.learning_preferences),
        'relaxation_methods': to_list(questionnaire.relaxation_methods),
    }
    return render(request, 'accounts/ans.html', context)


@login_required
def questionnaire_view(request):
    user = request.user

    if request.method == 'POST':
        data = request.POST

        # Check if user already has a questionnaire entry
        questionnaire, created = UserQuestionnaire.objects.get_or_create(user=user)

        # Set 1: Comma-separated text fields
        questionnaire.hobbies = data.get('hobbies', '')
        questionnaire.college_events = data.get('college_events', '')
        questionnaire.weekend_plans = data.get('weekend_plans', '')
        questionnaire.friendship_values = data.get('friendship_values', '')
        questionnaire.content_posting = data.get('content_posting', '')
        questionnaire.college_excitements = data.get('college_excitements', '')
        questionnaire.learning_preferences = data.get('learning_preferences', '')
        questionnaire.relaxation_methods = data.get('relaxation_methods', '')

        # Set 2: Single Choice
        questionnaire.introvert_extrovert = data.get('introvert_extrovert')
        questionnaire.first_meet = data.get('first_meet')
        questionnaire.sleep_type = data.get('sleep_type')
        questionnaire.important_trait = data.get('important_trait')
        questionnaire.year = data.get('year')
        questionnaire.comm_style = data.get('comm_style')
        questionnaire.posting_frequency = data.get('posting_frequency')
        questionnaire.decision_style = data.get('decision_style')
        questionnaire.free_time = data.get('free_time')

        # Set 3: Relationship Intent
        questionnaire.relationship_status = data.get('relationship_status')
        questionnaire.dating_approach = data.get('dating_approach')
        questionnaire.compatibility = data.get('compatibility')
        questionnaire.similar_interests = data.get('similar_interests')
        questionnaire.relationship_view = data.get('relationship_view')

        user.has_answered_questionnaire = True
        user.save()
        questionnaire.save()
        messages.success(request, "Preferences saved successfully!")
        return redirect('feed:home')  # or wherever you want to redirect

    else:
        # Prefill the form if data exists
        try:
            questionnaire = UserQuestionnaire.objects.get(user=user)
        except UserQuestionnaire.DoesNotExist:
            questionnaire = None

    return render(request, 'questionnaire_form.html', {
        'questionnaire': questionnaire,
    })


@login_required
def edit_profile(request):
    user = request.user
    questionnaire, created = UserQuestionnaire.objects.get_or_create(user=user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        bio = request.POST.get('bio')
        department = request.POST.get('department')
        year = request.POST.get('year')
        profile_picture = request.FILES.get('profile_picture')

        # Update user fields
        user.full_name = full_name
        user.bio = bio
        user.department = department
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()

        # Update questionnaire year
        questionnaire.year = year
        questionnaire.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('feed:profile', user_id=request.user.id)


    return render(request, 'accounts/edit_profile.html', {
        'user': user,
        'questionnaire': questionnaire
    })
