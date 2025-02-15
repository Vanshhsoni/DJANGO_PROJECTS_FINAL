from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.http import JsonResponse
from .models import Post, Comment  # Adjust according to your model structure
from feed import views 
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm

# Create your views here.


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assuming you have a user field in your Post model
            post.save()
            return redirect('feed:feed_home')  # Make sure to use the namespaced name
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})

@login_required
def feed_home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed_home.html', {'posts': posts})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        # Toggle the like
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Remove like if already liked
        else:
            post.likes.add(request.user)  # Add like if not liked yet
    return redirect('feed:feed_home')  # Redirect to the home/feed page


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(
                post=post,
                user=request.user,
                comment_text=comment_text
            )
    return redirect('feed:feed_home')

def feed_home(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'feed_home.html', {'posts': posts})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "GET":
        # Render the edit post form/template
        return render(request, 'edit_post.html', {'post': post})
    # Handle the post edit logic here, like updating the post

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('feed:feed_home') 
    
    
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        caption = request.POST.get('caption')  # Get the updated caption from form
        # Update the post's caption
        post.caption = caption
        post.save()
        # Redirect to the homepage or wherever after saving
        return redirect('feed:feed_home')
    # GET method case (showing the edit form)
    # return render(request, 'edit_template.html', {'post': post})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm  # Make sure this form is correctly defined
from .models import Profile  # Import the Profile model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile view for viewing a user's profile
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'profile_user': user,
    }
    return render(request, 'profile.html', {'profile_user': user})

# Edit profile view for updating the user's own profile
@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('feed:profile_view', username=user.username)
    else:
        form = ProfileForm(instance=user.profile)
    
    return render(request, 'edit_profile.html', {'form': form, 'user': user})


# Signal handlers for creating and saving user profiles
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # Create a profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=instance)
    if created:
        # Optional: initialize defaults for new profiles
        profile.bio = ""
        profile.profile_picture = 'default.jpg'  # Use your default image path
        profile.save()


from django.http import JsonResponse
from django.shortcuts import render
from .models import User  # Make sure to import your User model

def search(request):
    return render(request, 'search.html')
@login_required
def search_profiles(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
        user_data = []
        for user in users:
            user_data.append({
                'username': user.username,
                'profile_pic': user.profile.profile_picture.url if user.profile.profile_picture else '/static/default_profile.png'
            })
        return JsonResponse(user_data, safe=False)
    return JsonResponse([], safe=False)

