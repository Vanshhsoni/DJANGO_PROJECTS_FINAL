from django.shortcuts import render, redirect, get_object_or_404
from .models import Adoption
from .forms import AdoptionForm
from feed.models import Report, Volunteer  # Ensure correct imports for related models
import json
from django.contrib import messages

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Load credentials from JSON
        with open('credential.json', 'r') as f:
            credentials = json.load(f)

        # Verify credentials
        if username == credentials['username'] and password == credentials['password']:
            request.session['is_admin'] = True
            return redirect('adminpanel:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'adminpanel/login.html')

# Admin Dashboard
def admin_dashboard(request):
    reports = Report.objects.all()
    return render(request, 'adminpanel/dashboard.html', {'reports': reports})

# Admin Logout
def admin_logout(request):
    request.session.flush()
    return redirect('landing_page')

# Display Adoption Posts
def adoption_list(request):
    adoptions = Adoption.objects.all()  # Fetch all available adoption posts
    return render(request, 'adminpanel/adoption_list.html', {'adoptions': adoptions})

# Admin: Add Adoption
def add_adoption(request):
    if request.method == 'POST':
        form = AdoptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:adoption_list')
    else:
        form = AdoptionForm()
    return render(request, 'adminpanel/add_adoption.html', {'form': form})

# Admin: Delete Adoption Post
from django.shortcuts import get_object_or_404, redirect
from .models import Adoption


# User: Display Adoption Posts
def user_adoption(request):
    adoptions = Adoption.objects.all()
    return render(request, 'adminpanel/adoption_list.html', {'adoptions': adoptions})

# Volunteer List
def volunteer_list(request):
    volunteers = Volunteer.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/volx.html', {'volunteers': volunteers})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Adoption  # Assuming `Adoption` is the model for adoption posts



# Delete an Adoption Post
def delete_adoption(request, pk):
    adoption = get_object_or_404(Adoption, pk=pk)  # Get the adoption object by primary key
    adoption.delete()  # Delete the object
    return redirect('adminpanel:adoption_list')  # Redirect back to the adoption list

