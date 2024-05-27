from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import time
from .models import Subscription, Order
from .utils import calculate_and_reduce_balance  # Import the utility function

def toggle_meal(request, subscription_id, meal_type):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    now = timezone.now().time()
    today = timezone.now().date()

    if meal_type == 'lunch' and time(0, 0) <= now <= time(9, 0):
        orders = Order.objects.filter(subscription=subscription, meal_type='Lunch', date=today)
        if not orders.exists():
            # Reduce balance if meal is taken
            calculate_and_reduce_balance(subscription, 'Lunch')
            Order.objects.create(subscription=subscription, date=today, meal_type='Lunch')
    elif meal_type == 'dinner' and time(0, 0) <= now <= time(15, 0):
        orders = Order.objects.filter(subscription=subscription, meal_type='Dinner', date=today)
        if not orders.exists():
            # Reduce balance if meal is taken
            calculate_and_reduce_balance(subscription, 'Dinner')
            Order.objects.create(subscription=subscription, date=today, meal_type='Dinner')
    elif meal_type == 'both' and time(0, 0) <= now <= time(9, 0):
        orders = Order.objects.filter(subscription=subscription, date=today)
        if not orders.exists():
            # Reduce balance if both meals are taken
            calculate_and_reduce_balance(subscription, 'Both')
            Order.objects.create(subscription=subscription, date=today, meal_type='Both')

    return redirect('subscription_detail', subscription_id=subscription.id)

def subscription_detail(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    return render(request, 'orders/subscription_detail.html', {'subscription': subscription})
