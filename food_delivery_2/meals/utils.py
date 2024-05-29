# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_subscription_confirmation(user, plan):
    subject = 'Subscription Confirmation'
    plain_message = f"Dear {user.username},\n\nThank you for subscribing to our {plan.name} plan.\n\nPlan Details:\n- Price: ${plan.price}\n- Duration: {plan.duration} days\n\nWe hope you enjoy our service!\n\nBest regards,\nMeal Service Team"
    html_message = render_to_string('emails/subscription_confirmation.html', {
        'user': user,
        'plan': plan,
    })
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)

def send_meal_off_confirmation(user, meal_type):
    subject = 'Meal Off Confirmation'
    plain_message = f"Dear {user.username},\n\nYour {meal_type} has been successfully turned off for today.\n\nBest regards,\nMeal Service Team"
    html_message = render_to_string('emails/meal_off_confirmation.html', {
        'user': user,
        'meal_type': meal_type,
    })
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)