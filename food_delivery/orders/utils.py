from decimal import Decimal

def calculate_and_reduce_balance(subscription, meal_type):
    # Assuming that the subscription balance is initialized to the total cost
    days_remaining = (subscription.end_date - subscription.start_date).days + 1
    daily_rate = subscription.balance / Decimal(subscription.customer.plan_days)

    if meal_type == 'Lunch':
        subscription.balance -= daily_rate / 2  # Half the daily rate for lunch
    elif meal_type == 'Dinner':
        subscription.balance -= daily_rate / 2  # Half the daily rate for dinner
    elif meal_type == 'Both':
        subscription.balance -= daily_rate  # Full daily rate for both

    subscription.save()
