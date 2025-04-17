from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.db import IntegrityError
from accounts.models import User, UserQuestionnaire

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Crush, Friendship
from django.db import models




# Helper function to compare compatibility
def compare_multiple_choice(user_answer, other_user_answer, max_points=5):
    user_answer_set = set([x.strip().lower() for x in user_answer.split(',')])
    other_user_answer_set = set([x.strip().lower() for x in other_user_answer.split(',')])
    
    match_count = len(user_answer_set.intersection(other_user_answer_set))
    if match_count == 0:
        return 0
    return (match_count / len(user_answer_set.union(other_user_answer_set))) * max_points


# Helper function to compare single-choice compatibility
def compare_single_choice(user_answer, other_user_answer, max_points=3):
    return max_points if user_answer == other_user_answer else 0


# View to list all users with compatibility scores
@login_required
def all_users(request):
    logged_in_user = request.user
    user_questionnaire = UserQuestionnaire.objects.get(user=logged_in_user)

    compatibility_scores = []
    other_users = User.objects.exclude(id=logged_in_user.id)

    for user in other_users:
        other_user_questionnaire = UserQuestionnaire.objects.get(user=user)
        compatibility_score = 0

        # Set 3: Relationship Intent (Most Weighting)
        compatibility_score += compare_single_choice(user_questionnaire.relationship_status, other_user_questionnaire.relationship_status, max_points=25)
        compatibility_score += compare_single_choice(user_questionnaire.dating_approach, other_user_questionnaire.dating_approach, max_points=20)
        compatibility_score += compare_single_choice(user_questionnaire.compatibility, other_user_questionnaire.compatibility, max_points=15)
        compatibility_score += compare_single_choice(user_questionnaire.relationship_view, other_user_questionnaire.relationship_view, max_points=15)
        compatibility_score += compare_single_choice(user_questionnaire.similar_interests, other_user_questionnaire.similar_interests, max_points=10)

        # Set 1: Multiple Choice Inputs (Medium Weighting)
        compatibility_score += compare_multiple_choice(user_questionnaire.hobbies, other_user_questionnaire.hobbies) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.college_events, other_user_questionnaire.college_events) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.weekend_plans, other_user_questionnaire.weekend_plans) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.friendship_values, other_user_questionnaire.friendship_values) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.content_posting, other_user_questionnaire.content_posting) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.college_excitements, other_user_questionnaire.college_excitements) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.learning_preferences, other_user_questionnaire.learning_preferences) * 5
        compatibility_score += compare_multiple_choice(user_questionnaire.relaxation_methods, other_user_questionnaire.relaxation_methods) * 5

        # Set 2: Single Choice Inputs (Least Weighting)
        compatibility_score += compare_single_choice(user_questionnaire.introvert_extrovert, other_user_questionnaire.introvert_extrovert) * 3
        compatibility_score += compare_single_choice(user_questionnaire.first_meet, other_user_questionnaire.first_meet) * 3
        compatibility_score += compare_single_choice(user_questionnaire.sleep_type, other_user_questionnaire.sleep_type) * 3
        compatibility_score += compare_single_choice(user_questionnaire.important_trait, other_user_questionnaire.important_trait) * 3
        compatibility_score += compare_single_choice(user_questionnaire.year, other_user_questionnaire.year) * 3
        compatibility_score += compare_single_choice(user_questionnaire.comm_style, other_user_questionnaire.comm_style) * 3
        compatibility_score += compare_single_choice(user_questionnaire.posting_frequency, other_user_questionnaire.posting_frequency) * 3
        compatibility_score += compare_single_choice(user_questionnaire.decision_style, other_user_questionnaire.decision_style) * 3
        compatibility_score += compare_single_choice(user_questionnaire.free_time, other_user_questionnaire.free_time) * 3

        # Capping the score to a maximum of 99% (realistic compatibility)
        compatibility_score = min(compatibility_score, 99)

        # Ensuring that the compatibility score never goes below 10%
        compatibility_score = max(compatibility_score, 10)

        # Add the user and their compatibility score to the list
        compatibility_scores.append((user, compatibility_score))

    # Sort the compatibility scores in descending order
    compatibility_scores.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'feed/all.html', {
        'compatibility_scores': compatibility_scores,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


from accounts.models import Crush, Friendship

@login_required
def home(request):
    current_user = request.user
    all_users = User.objects.exclude(id=current_user.id)

    def get_crush_status(person):
        sent = Crush.objects.filter(sender=current_user, receiver=person).first()
        received = Crush.objects.filter(sender=person, receiver=current_user).first()
        if sent and received and sent.is_mutual and received.is_mutual:
            return "mutual"
        elif sent:
            return "sent"
        elif received:
            return "received"
        return "none"

    # Recently joined
    recently_joined = all_users.filter(date_joined__gte=timezone.now() - timedelta(days=7))[:10]
    trending = all_users.order_by('-date_joined')[:10]

    same_year = []
    try:
        user_year = current_user.questionnaire.year
        same_year_questionnaires = UserQuestionnaire.objects.filter(year=user_year).exclude(user=current_user)
        same_year = [uq.user for uq in same_year_questionnaires][:10]
    except UserQuestionnaire.DoesNotExist:
        pass

    same_department = all_users.filter(department=current_user.department)[:10]
    same_college = all_users.filter(college=current_user.college)[:10]

    # Crush stats
    hearts_sent = Crush.objects.filter(sender=current_user, is_mutual=False).count()
    hearts_received = Crush.objects.filter(receiver=current_user, is_mutual=False).count()
    friends = Friendship.objects.filter(models.Q(user1=current_user) | models.Q(user2=current_user)).count()

    # Add crush status mapping for each group
    def annotate_users_with_crush(users):
        return [
            {
                'user': person,
                'crush_status': get_crush_status(person)
            } for person in users
        ]

    context = {
        'recently_joined': annotate_users_with_crush(recently_joined),
        'trending': annotate_users_with_crush(trending),
        'same_year': annotate_users_with_crush(same_year),
        'same_department': annotate_users_with_crush(same_department),
        'same_college': annotate_users_with_crush(same_college),
        'hearts_sent': hearts_sent,
        'hearts_received': hearts_received,
        'friends': friends,
        'profile_views': 0,
        'unfriended_recently': 0,
        'notifications': 0,
        'top_matches': 0,
        'recent_friends': 0,
    }

    return render(request, 'feed/home.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    # Check crush status without filtering by is_mutual
    sent_crush = Crush.objects.filter(sender=request.user, receiver=profile_user).exists()
    received_crush = Crush.objects.filter(sender=profile_user, receiver=request.user).exists()
    
    # Check if both users have sent crushes to each other and at least one is marked mutual
    is_mutual = False
    if sent_crush and received_crush:
        sent_crush_obj = Crush.objects.get(sender=request.user, receiver=profile_user)
        received_crush_obj = Crush.objects.get(sender=profile_user, receiver=request.user)
        is_mutual = sent_crush_obj.is_mutual or received_crush_obj.is_mutual
    
    if request.method == 'POST':
        crush_action = request.POST.get('crush_action')

        if crush_action == 'send_crush':
            # Only create if it doesn't exist
            if not sent_crush:
                crush = Crush.objects.create(sender=request.user, receiver=profile_user)
                # Check if this creates a mutual crush
                crush.check_mutual_and_create_friendship()
                messages.success(request, "Crush sent! 💘")
            else:
                messages.info(request, "You've already sent a crush.")
            
        elif crush_action == 'accept_crush':
            if received_crush and not sent_crush:
                # Create the return crush
                crush = Crush.objects.create(sender=request.user, receiver=profile_user)
                # This will handle setting both to mutual and creating friendship
                crush.check_mutual_and_create_friendship()
                messages.success(request, "Crush accepted! It's a match! 💖")
            else:
                messages.error(request, "No crush to accept.")
                
        elif crush_action == 'uncrush':
            # Remove the crush regardless of mutual status
            Crush.objects.filter(sender=request.user, receiver=profile_user).delete()
            
            # If there was a mutual relationship, update the other person's crush
            if is_mutual:
                other_crush = Crush.objects.filter(sender=profile_user, receiver=request.user).first()
                if other_crush:
                    other_crush.is_mutual = False
                    other_crush.save()
            
            messages.success(request, "Crush removed 💔")
            
        return redirect('feed:profile', user_id=user_id)

    return render(request, 'feed/profile.html', {
        'profile_user': profile_user,
        'sent_crush': sent_crush,
        'received_crush': received_crush,
        'is_mutual': is_mutual,  # Changed from mutual_crush to is_mutual to match template
    })




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Crush, Friendship  # Import your Crush and Friendship models
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def crush_action(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    # Don't allow sending crush to yourself
    if profile_user == request.user:
        messages.error(request, "You cannot send a crush to yourself.")
        return redirect('feed:profile', user_id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('crush_action')

        # Handle Send Crush action
        if action == 'send_crush':
            # Check if crush already exists
            existing_crush = Crush.objects.filter(sender=request.user, receiver=profile_user).first()
            
            if not existing_crush:
                # Create new crush
                crush = Crush.objects.create(sender=request.user, receiver=profile_user)
                # Check if there's a mutual crush and handle friendship creation
                crush.check_mutual_and_create_friendship()
                messages.success(request, 'Crush sent! 💘')
            else:
                messages.info(request, 'You already sent a crush.')

        # Handle Accept Crush action
        elif action == 'accept_crush':
            # First check if they sent us a crush
            received_crush = Crush.objects.filter(sender=profile_user, receiver=request.user).first()
            
            if received_crush:
                # Create the reverse crush
                crush, created = Crush.objects.get_or_create(sender=request.user, receiver=profile_user)
                
                # Update both crushes to mutual
                received_crush.is_mutual = True
                crush.is_mutual = True
                received_crush.save()
                crush.save()
                
                # Create friendship if it doesn't exist
                if not Friendship.are_friends(request.user, profile_user):
                    Friendship.objects.get_or_create(user1=request.user, user2=profile_user)
                
                messages.success(request, 'It\'s a match! 💖 You\'re now friends!')
            else:
                messages.error(request, 'No crush to accept.')

        # Handle Uncrush action
        elif action == 'uncrush':
            # Remove the crush from sender to receiver
            crush_sent = Crush.objects.filter(sender=request.user, receiver=profile_user).first()
            if crush_sent:
                crush_sent.delete()
                
                # If there was a mutual crush, set the reverse crush to not mutual
                crush_received = Crush.objects.filter(sender=profile_user, receiver=request.user).first()
                if crush_received:
                    crush_received.is_mutual = False
                    crush_received.save()
                
                messages.success(request, 'Crush removed 💔')
            else:
                messages.info(request, 'No crush to remove.')

        return redirect('feed:profile', user_id=user_id)

    # If not POST request
    return HttpResponse("Invalid request", status=400)