from django.db import models
from django.contrib.auth.models import User

    
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        (3, '3 Days'),
        (7, '7 Days'),
        (15, '15 Days'),
        (30, '30 Days'),
    ]
    name = models.CharField(max_length=50)
    duration = models.IntegerField(choices=PLAN_CHOICES)  # Duration in days
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lunch_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dinner_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
 
class Customer(models.Model):
    CATEGORY_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username


class MealOff(models.Model):
    MEAL_CHOICES = [
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES, null=True, blank=True)
    lunch_off = models.BooleanField(default=False)
    dinner_off = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.user.username} - {self.date} - {self.meal_type}"


class OrderStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    lunch_basic = models.IntegerField(default=0)
    lunch_premium = models.IntegerField(default=0)
    dinner_basic = models.IntegerField(default=0)
    dinner_premium = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)