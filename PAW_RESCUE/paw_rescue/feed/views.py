from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report  # Import only once
from .forms import ReportForm

@login_required
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)  # Create a Report instance but don't save yet
            report.user = request.user  # Assign the logged-in user to the report
            report.save()  # Save the report
            return redirect('feed')  # Redirect to the feed page
    else:
        form = ReportForm()  # Initialize an empty form for GET requests

    return render(request, 'feed/report.html', {'form': form})  # Render the report form page

@login_required
def feed(request):
    reports = Report.objects.all()
    report_count = reports.count()  # Count the total number of reports
    volunteers = Volunteer.objects.all()
    volunteer_count=volunteers.count()
    adoptions = Adoption.objects.all()
    adoption_requests_count=adoptions.count()
    return render(request, 'feed/feed.html', {'reports': reports, 'report_count': report_count, 'volunteer_count':volunteer_count, 'adoption_requests_count':adoption_requests_count})

from django.shortcuts import render
from adminpanel.models import Adoption

def adoption_public(request):
    adoptions = Adoption.objects.all()  # Fetch all adoption posts
    return render(request, 'feed/adopt_public.html', {'adoptions': adoptions})

from django.shortcuts import render, redirect
from .forms import VolunteerForm
from .models import Volunteer

from django.shortcuts import render, redirect
from .forms import VolunteerForm

def volunteer_form(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')  # Redirect to a thank-you page after submission
    else:
        form = VolunteerForm()
    return render(request, 'feed/voll.html', {'form': form})

def food(request):
    return render(request, 'feed/food.html')

import json
import os
from django.shortcuts import render

def health(request):
    # Construct the path to health.json in the root directory
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'health.json')
    
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the 'items' key
    health_data = data.get('items', [])
    
    # Pass the JSON data to the template
    return render(request, 'feed/health.html', {'health_data': health_data})

# views.py
import json
from django.shortcuts import render
from django.http import Http404

import os
import json
from django.shortcuts import render
from django.http import Http404

def food_view(request):
    try:
        # Construct the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'food.json')
        
        # Open and load the JSON data
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise Http404("Food data not found.")
    except json.JSONDecodeError:
        raise Http404("Invalid JSON format in the food data file.")

    # Pass the data to the template
    return render(request, "feed/food.html", {"animals": data})

def donate(request):
    return render(request, 'feed/donate.html')

def location(request):
    return render(request, 'feed/location.html')