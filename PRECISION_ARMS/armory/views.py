from django.shortcuts import render

# Create your views here.

def armory_home(request):
    return render(request, 'armory/armory_home.html')

def DMR(request):
    return render(request, 'armory/shop_dmr.html')

def ETC(request):
    return render(request, 'armory/shop_etc.html')

def HANDGUN(request):
    return render(request, 'armory/shop_handgun.html')

def MELEE(request):
    return render(request, 'armory/shop_melee.html')

def SHOTGUN(request):
    return render(request, 'armory/shop_shotgun.html')

def SMG(request):
    return render(request, 'armory/shop_smg.html')

def SR(request):
    return render(request, 'armory/shop_sr.html')

def THROWABLE(request):
    return render(request, 'armory/shop_throwable.html')

def AR(request):
    return render(request, 'armory/shop.html')


# BUYING PROPERTIES BELOW
import json
from django.shortcuts import render
from django.http import Http404

def buy_load(request, weapon_name):
    print("buy_load function is called")  # This will confirm if the view is hit
    print(f"Weapon Name: {weapon_name}")  # This will print the weapon name in the terminal

    # Load the JSON data from the file
    try:
        with open('static/json/guns.json') as json_file:
            guns = json.load(json_file)
    except FileNotFoundError:
        print("JSON file not found.")
        return Http404("Guns data not found.")

    # Find the weapon that matches the weapon_name
    gun = next((gun for gun in guns if gun["name"] == weapon_name), None)

    if gun is None:
        print("Weapon not found in the JSON data.")
        return Http404("Weapon not found.")

    context = {
        'gun': gun,  # Pass the matched gun details to the template
        'weapon_name': weapon_name,  # Optional: pass to the template if needed
    }
    
    return render(request, 'buy_page.html', context)

def ATTACHMENTS_MAIN(request):
    return render(request, 'attachments/main.html')

def ABOUT_US(request):
    return render(request, 'about_us.html')