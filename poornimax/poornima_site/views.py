from django.shortcuts import render

def home(request):
    return render(request, 'poornima_site/index.html')
