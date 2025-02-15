import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order
from django.views.decorators.csrf import csrf_exempt

@login_required
def buy_weapon(request, weapon_name):
    # Get the gun details from the JSON file
    try:
        with open('static/json/guns.json') as json_file:
            guns = json.load(json_file)
        gun = next((gun for gun in guns if gun["name"] == weapon_name), None)

        if gun is None:
            return Http404("Weapon not found.")

        # Check if the order already exists for this user and weapon
        order, created = Order.objects.get_or_create(
            user=request.user,
            weapon_name=gun["name"],
            weapon_image=gun["image"],
            defaults={'quantity': 1}  # Create with a default quantity of 1 if it doesn't exist
        )

        if not created:
            # If the order already exists, increase the quantity
            order.quantity += 1
            order.save()

        return redirect('orders:show_orders')

    except FileNotFoundError:
        return Http404("Guns data not found.")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order  # Import your Order model

@login_required
def show_orders(request):
    orders = Order.objects.filter(user=request.user)
    
    # Check if the user has an associated profile
    user_profile = request.user.profile if hasattr(request.user, 'profile') else None

    context = {
        'orders': orders,
        'user': request.user,
        'user_profile': user_profile,  # Pass the profile data to the template
    }

    return render(request, 'orders/show_orders.html', context)



from django.contrib.auth.decorators import login_required
from .models import OrderedOrders

@login_required
def previous_orders(request):
    # Fetch the previous orders for the logged-in user
    ordered_orders = OrderedOrders.objects.filter(user=request.user)

    # Render the template and pass the ordered orders to the context
    return render(request, 'orders/previous.html', {'ordered_orders': ordered_orders})


@csrf_exempt
def delete_order(request, weapon_id):
    if request.method == 'DELETE':
        try:
            order = Order.objects.get(id=weapon_id)
            order.delete()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

@csrf_exempt  # Replace with proper CSRF handling in production
def update_order_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        weapon_id = data.get('weapon_id')
        quantity = data.get('quantity')

        order = get_object_or_404(Order, id=weapon_id)
        order.quantity = quantity
        order.save()

        return JsonResponse({'status': 'success', 'quantity': order.quantity})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def confirm_order(request):
    from .models import OrderedOrders, Order
    from django.utils import timezone

    # Fetch the orders for the logged-in user from the Order model
    orders = Order.objects.filter(user=request.user)

    # Create OrderedOrders instances from the fetched orders
    for order in orders:
        # Create an instance of OrderedOrders with data from Order
        ordered_order = OrderedOrders(
            user=order.user,
            weapon_name=order.weapon_name,
            weapon_image=order.weapon_image,
            quantity=order.quantity,
            order_date=order.order_date,
            confirmed_date=timezone.now()  # Set the confirmed date to the current time
        )
        # Save the ordered_order instance to the database
        ordered_order.save()
    orders.delete()
    # Fetch the ordered orders after saving
    ordered_orders = OrderedOrders.objects.filter(user=request.user)

    # Render the confirmation page and pass the ordered orders to the template
    return render(request, 'orders/confirm.html', {'ordered_orders': ordered_orders})
