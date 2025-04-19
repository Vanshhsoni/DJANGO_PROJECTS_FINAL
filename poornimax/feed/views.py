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
from django.utils.timesince import timesince

from django.db import models
from datetime import datetime 




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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timesince import timesince
from .forms import *
from .models import *

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
    
    # Get user's posts
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    
    # Get the latest post
    latest_post = posts.first()
    
    # Add like and comment counts to posts
    for post in posts:
        post.likes_count = Like.objects.filter(post=post).count()
        post.comments_count = Comment.objects.filter(post=post).count()
    
    context = {
        'profile_user': profile_user,
        'sent_crush': sent_crush,
        'received_crush': received_crush,
        'is_mutual': is_mutual,
        'posts': posts,
        'latest_post': latest_post,
    }
    
    return render(request, 'feed/profile.html', context)

# Add this to feed/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('feed:profile', user_id=request.user.id)
    else:
        form = PostForm()
    
    return render(request, 'feed/create_post.html', {'form': form})

# Add these to feed/views.py
@login_required
def explore(request):
    query = request.GET.get('q', '')
    users = []
    
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:20]
    
    # Get recent confessions
    confessions = Confession.objects.all()[:20]
    
    return render(request, 'feed/explore.html', {
        'query': query,
        'users': users,
        'confessions': confessions
    })

@login_required
def create_confession(request):
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
            confession = form.save(commit=False)
            
            # Only store user reference if not anonymous
            if not confession.is_anonymous:
                confession.user = request.user
            
            confession.save()
            messages.success(request, "Confession posted successfully!")
            return redirect('feed:explore')
    else:
        form = ConfessionForm(initial={'is_anonymous': True})
    
    return render(request, 'feed/confession.html', {'form': form})

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        # Check if already liked
        like_exists = Like.objects.filter(post=post, user=request.user).exists()
        
        if like_exists:
            # Unlike
            Like.objects.filter(post=post, user=request.user).delete()
            liked = False
        else:
            # Like
            Like.objects.create(post=post, user=request.user)
            liked = True
        
        # Redirect to the profile page of the post owner
        return redirect('feed:profile', user_id=post.user.id)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            
            # Redirect to the profile page of the post owner
            return redirect('feed:profile', user_id=post.user.id)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        post_user_id = comment.post.user.id
        
        # Only comment owner or post owner can delete
        if request.user == comment.user or request.user == comment.post.user:
            comment.delete()
            # Redirect to the profile page of the post owner
            return redirect('feed:profile', user_id=post_user_id)
        
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post_user_id = post.user.id
        
        # Only post owner can delete their post
        if request.user == post.user:
            post.delete()
            # Redirect to the profile page of the post owner
            return redirect('feed:profile', user_id=post_user_id)
        
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def get_post_data(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user can view this post
    profile_user = post.user
    sent_crush = Crush.objects.filter(sender=request.user, receiver=profile_user).exists()
    received_crush = Crush.objects.filter(sender=profile_user, receiver=request.user).exists()
    
    is_mutual = False
    if sent_crush and received_crush:
        sent_crush_obj = Crush.objects.get(sender=request.user, receiver=profile_user)
        received_crush_obj = Crush.objects.get(sender=profile_user, receiver=request.user)
        is_mutual = sent_crush_obj.is_mutual or received_crush_obj.is_mutual
    
    # Check if user can see this post
    if not (request.user == profile_user or is_mutual):
        return JsonResponse({'success': False, 'error': 'Not authorized'})
    
    # Get comments
    comments = []
    for comment in Comment.objects.filter(post=post).order_by('-created_at'):
        comments.append({
            'id': comment.id,
            'username': comment.user.username,
            'user_id': comment.user.id,
            'user_image': comment.user.profile_picture.url,
            'content': comment.content,
            'time': timesince(comment.created_at),
            'is_owner': comment.user == request.user,
            'can_delete': comment.user == request.user or post.user == request.user
        })
    
    # Check if user has liked this post
    liked = Like.objects.filter(post=post, user=request.user).exists()
    likes_count = Like.objects.filter(post=post).count()
    
    return JsonResponse({
        'success': True,
        'post': {
            'id': post.id,
            'image': post.image.url,
            'caption': post.caption,
            'time': timesince(post.created_at),
            'username': post.user.username,
            'user_id': post.user.id,
            'user_image': post.user.profile_picture.url,
            'liked': liked,
            'likes_count': likes_count,
            'comments': comments,
            'is_owner': post.user == request.user
        }
    })
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user can view this post
    profile_user = post.user
    sent_crush = Crush.objects.filter(sender=request.user, receiver=profile_user).exists()
    received_crush = Crush.objects.filter(sender=profile_user, receiver=request.user).exists()
    
    is_mutual = False
    if sent_crush and received_crush:
        sent_crush_obj = Crush.objects.get(sender=request.user, receiver=profile_user)
        received_crush_obj = Crush.objects.get(sender=profile_user, receiver=request.user)
        is_mutual = sent_crush_obj.is_mutual or received_crush_obj.is_mutual
    
    # Check if user can see this post
    if not (request.user == profile_user or is_mutual):
        return JsonResponse({'success': False, 'error': 'Not authorized'})
    
    # Get comments
    comments = []
    for comment in Comment.objects.filter(post=post):
        comments.append({
            'id': comment.id,
            'username': comment.user.username,
            'user_id': comment.user.id,
            'user_image': comment.user.profile_picture.url,
            'content': comment.content,
            'time': timesince(comment.created_at),
            'is_owner': comment.user == request.user,
            'can_delete': comment.user == request.user or post.user == request.user
        })
    
    # Check if user has liked this post
    liked = Like.objects.filter(post=post, user=request.user).exists()
    likes_count = Like.objects.filter(post=post).count()
    
    return JsonResponse({
        'success': True,
        'post': {
            'id': post.id,
            'image': post.image.url,
            'caption': post.caption,
            'time': timesince(post.created_at),
            'username': post.user.username,
            'user_id': post.user.id,
            'user_image': post.user.profile_picture.url,
            'liked': liked,
            'likes_count': likes_count,
            'comments': comments,
            'is_owner': post.user == request.user
        }
    })