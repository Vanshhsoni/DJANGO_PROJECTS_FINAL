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
    return render(request, 'feed/feed.html', {'reports': reports, 'report_count': report_count})

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