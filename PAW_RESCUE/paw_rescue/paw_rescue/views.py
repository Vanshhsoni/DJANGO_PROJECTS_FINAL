from django.shortcuts import render
from feed.models import Report
def landing_page(request):
    return render(request, "landing.html")
