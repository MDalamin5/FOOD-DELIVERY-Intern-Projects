from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import time
from .models import Subscription, Order
from django.db.models import Count
from .utils import calculate_and_reduce_balance  # Import the utility function

def toggle_meal(request, subscription_id, meal_type):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    # now = timezone.now().time()
    
    now = timezone.localtime(timezone.now()).time()
    today = timezone.now().date()
    
    print('current timeeeeeee---', now, 'current-day',today)

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



def order_counts_daily(request):
    # Get today's date
    today = timezone.now().date()
    
    # Query to count daily orders for basic and premium subscriptions, separated by lunch and dinner
    basic_lunch_count = Order.objects.filter(date=today, subscription__customer__category='Basic', meal_type='Lunch').count()
    basic_dinner_count = Order.objects.filter(date=today, subscription__customer__category='Basic', meal_type='Dinner').count()
    premium_lunch_count = Order.objects.filter(date=today, subscription__customer__category='Premium', meal_type='Lunch').count()
    premium_dinner_count = Order.objects.filter(date=today, subscription__customer__category='Premium', meal_type='Dinner').count()
    
    # Create a dictionary to store the counts
    order_counts = {
        'basic_lunch': basic_lunch_count,
        'basic_dinner': basic_dinner_count,
        'premium_lunch': premium_lunch_count,
        'premium_dinner': premium_dinner_count,
    }
    
    return render(request, 'orders/order_counts_daily.html', {'order_counts': order_counts})
