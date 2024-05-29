from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import time
from .forms import SignUpForm, MealOffForm
from .models import MealOff, Customer, SubscriptionPlan
from django.contrib.auth import logout

from django.shortcuts import render
from .models import OrderStatistics
from django.db.models import Count
from django.utils import timezone
from .utils import send_subscription_confirmation, send_meal_off_confirmation


from django.shortcuts import render

from django.shortcuts import render
from .models import SubscriptionPlan

@login_required
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    user = request.user

    # Check if the user is authenticated and has a subscription plan
    try:
        customer = Customer.objects.get(user=user)
        current_plan = customer.subscription_plan
    except Customer.DoesNotExist:
        current_plan = None

    return render(request, 'meals/subscription_plans.html', {'plans': plans, 'current_plan': current_plan})


def home(request):
    
    # plans = SubscriptionPlan.objects.all()
    # for plan in plans:
    #     print(plan.id, plan.name, plan.price)

    return render(request, 'meals/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('subscription_plans')  # Redirect to the login page after sign up
    else:
        form = SignUpForm()
    return render(request, 'meals/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'meals/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

# @login_required
# def meal_off(request):
#     now = timezone.localtime(timezone.now())
#     current_time = now.time()

#     if request.method == 'POST':
#         form = MealOffForm(request.POST)
#         if form.is_valid():
#             meal_off = form.save(commit=False)
#             meal_off.customer = Customer.objects.get(user=request.user)

#             if meal_off.lunch_off and meal_off.dinner_off:
#                 if not (time(0, 0) <= current_time <= time(9, 0)):
#                     return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Both meals can only be turned off between 12 AM and 9 AM.'})
#             elif meal_off.lunch_off:
#                 if not (time(0, 0) <= current_time <= time(9, 0)):
#                     return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Lunch can only be turned off between 12 AM and 9 AM.'})
#             elif meal_off.dinner_off:
#                 if not (time(0, 0) <= current_time <= time(15, 0)):
#                     return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Dinner can only be turned off between 12 AM and 3 PM.'})

#             meal_off.save()
#             return redirect('meal_off_success')
#     else:
#         form = MealOffForm()

#     return render(request, 'meals/meal_off.html', {'form': form})


@login_required
def meal_off_success(request):
    return render(request, 'meals/meal_off_success.html')


@login_required
def meal_off(request):
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    today = now.date()

    if request.method == 'POST':
        form = MealOffForm(request.POST)
        if form.is_valid():
            meal_off = form.save(commit=False)
            customer = Customer.objects.get(user=request.user)
            meal_off.customer = customer

            # Check if the meal is already turned off for today
            if MealOff.objects.filter(customer=customer, date=today).exists():
                return render(request, 'meals/meal_off.html', {
                    'form': form,
                    'error': 'You have already turned off meals for today.'
                })

            if meal_off.lunch_off and meal_off.dinner_off:
                if not (time(0, 0) <= current_time <= time(9, 0)):
                    return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Both meals can only be turned off between 12 AM and 9 AM.'})
            elif meal_off.lunch_off:
                if not (time(0, 0) <= current_time <= time(9, 0)):
                    return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Lunch can only be turned off between 12 AM and 9 AM.'})
            elif meal_off.dinner_off:
                if not (time(0, 0) <= current_time <= time(15, 0)):
                    return render(request, 'meals/meal_off.html', {'form': form, 'error': 'Dinner can only be turned off between 12 AM and 3 PM.'})

            meal_off.date = today  # Set the date to today
            meal_off.save()
            
            # Send confirmation email
            meal_types = []
            if meal_off.lunch_off:
                meal_types.append('lunch')
            if meal_off.dinner_off:
                meal_types.append('dinner')
            for meal_type in meal_types:
                send_meal_off_confirmation(request.user, meal_type)

            return redirect('meal_off_success')
    else:
        form = MealOffForm()

    return render(request, 'meals/meal_off.html', {'form': form})



from django.contrib.auth.models import User
from .models import Customer, SubscriptionPlan

from decimal import Decimal
def convert_to_customer(user):
    # Assign a default subscription plan if needed
    default_plan = SubscriptionPlan.objects.first()
    
    # Create a new customer instance for the user
    return Customer.objects.create(
        user=user,
        category='Basic',  # or any default category you want to assign
        balance=Decimal('500.00')  # initial balance
    )





# @login_required
# def subscribe(request, plan_id):
#     user = request.user
#     plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
#     try:
#         # Check if the user is a customer
#         customer = Customer.objects.get(user=user)
#     except Customer.DoesNotExist:
#         # If not, convert the user to a customer
#         customer = convert_to_customer(user)
    
#     # Ensure that the plan price is a Decimal
#     plan_price = Decimal(plan.price)
    
#     # Update the customer's subscription plan and balance
#     customer.subscription_plan = plan
#     customer.balance -= plan_price
#     customer.save()
    
#     return render(request, 'meals/subscribe_success.html', {'plan': plan})





@login_required
def subscribe(request, plan_id):
    user = request.user
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = convert_to_customer(user)
    
    if customer.subscription_plan:
        current_plan = customer.subscription_plan
        return render(request, 'meals/subscribe.html', {
            'plan': plan,
            'current_plan': current_plan,
            'message': 'You already have a subscription plan. You cannot change it unless you pay 50% of the current plan\'s price.'
        })
    
    plan_price = Decimal(plan.price)
    
    if customer.balance < plan_price:
        return render(request, 'meals/subscribe.html', {
            'plan': plan,
            'message': 'Insufficient balance to subscribe to this plan.'
        })
    
    customer.subscription_plan = plan
    customer.balance -= plan_price
    customer.save()
    
    send_subscription_confirmation(user, plan)  # Send subscription confirmation email
    
    return render(request, 'meals/subscribe_success.html', {'plan': plan})



@login_required
def consume_meal(request, meal_type):
    customer = Customer.objects.get(user=request.user)

    # Check if the customer has a subscription plan
    if not customer.subscription_plan:
        return render(request, 'meals/no_subscription.html')

    # Check the current time
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    today = now.date()

    # Determine the price to deduct based on the meal type
    if meal_type == 'lunch' and (time(0, 0) <= current_time <= time(9, 0)):
        meal_price = customer.subscription_plan.lunch_price
        meal_time = 'lunch'
    elif meal_type == 'dinner' and (time(0, 0) <= current_time <= time(15, 0)):
        meal_price = customer.subscription_plan.dinner_price
        meal_time = 'dinner'
    elif meal_type == 'both' and (time(0, 0) <= current_time <= time(9, 0)):
        meal_price = customer.subscription_plan.lunch_price + customer.subscription_plan.dinner_price
        meal_time = 'both'
    else:
        return render(request, 'meals/invalid_meal_time.html')

    # Deduct the meal price from the customer's balance
    if customer.balance >= meal_price:
        customer.balance -= meal_price
        customer.save()

        # Update OrderStatistics
        stats, created = OrderStatistics.objects.get_or_create(date=today)
        if customer.category == 'Basic':
            if meal_time == 'lunch' or meal_time == 'both':
                stats.lunch_basic += 1
            if meal_time == 'dinner' or meal_time == 'both':
                stats.dinner_basic += 1
        elif customer.category == 'Premium':
            if meal_time == 'lunch' or meal_time == 'both':
                stats.lunch_premium += 1
            if meal_time == 'dinner' or meal_time == 'both':
                stats.dinner_premium += 1
        stats.save()

        return redirect('consume_meal_success')
    else:
        return render(request, 'meals/insufficient_balance.html')
















@login_required
def subscription_success(request):
    return render(request, 'meals/subscription_success.html')

@login_required
def consume_meal_success(request):
    return render(request, 'meals/consume_meal_success.html')

@login_required
def invalid_meal_time(request):
    return render(request, 'meals/invalid_meal_time.html')



# admin panel views

from .models import OrderStatistics
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def order_statistics_view(request):
    # Get today's date
    today = timezone.localtime(timezone.now()).date()
    
    # Fetch statistics for today
    stats, created = OrderStatistics.objects.get_or_create(date=today)
    
    # Render the template with the statistics
    context = {
        'stats': stats
    }
    
    return render(request, 'meals/order_statistics.html', context)





@login_required
def meal_order_info(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    meal_offs = MealOff.objects.filter(customer=customer)

    return render(request, 'meals/meal_order_info.html', {'meal_offs': meal_offs})

