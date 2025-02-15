from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect
import json
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Load credentials from JSON
        with open('credential.json', 'r') as f:
            credentials = json.load(f)

        # Verify credentials
        if username == credentials['username'] and password == credentials['password']:
            request.session['is_admin'] = True  # Mark admin as logged in
            return redirect('adminpanel:admin_dashboard')  # Correctly namespaced URL
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'adminpanel/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Load credentials from JSON
        with open('credential.json', 'r') as f:
            credentials = json.load(f)

        # Verify credentials
        if username == credentials['username'] and password == credentials['password']:
            request.session['is_admin'] = True  # Mark admin as logged in
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'adminpanel/login.html')

from django.shortcuts import render
from feed.models import Report  # Import the Report model

def admin_dashboard(request):
    reports = Report.objects.all()  # Fetch all reports from the feed app
    return render(request, 'adminpanel/dashboard.html', {'reports': reports})


def admin_logout(request):
    request.session.flush()  # Clear the session
    return redirect('landing_page')

#admin post X X X

from django.shortcuts import render, redirect, get_object_or_404
from .models import Adoption
from .forms import AdoptionForm

# Admin: Add Adoption
def add_adoption(request):
    if request.method == 'POST':
        form = AdoptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:admin_dashboard')
  # Redirect to admin dashboard
    else:
        form = AdoptionForm()
    return render(request, 'adminpanel/add_adoption.html', {'form': form})


# Admin: Delete Adoption Post
def delete_adoption(request, pk):
    adoption = get_object_or_404(Adoption, pk=pk)
    adoption.delete()
    return redirect('admin_dashboard')

# User: Display Adoption Posts
def user_adoption(request):
    adoptions = Adoption.objects.all()
    return render(request, 'adminpanel/adopt.html', {'adoptions': adoptions})

from django.shortcuts import render
from feed.models import Volunteer

def volunteer_list(request):
    volunteers = Volunteer.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/volx.html', {'volunteers': volunteers})