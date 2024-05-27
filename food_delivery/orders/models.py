from django.db import models

class Customer(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    CATEGORY_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium')
    ]
    PLAN_CHOICES = [
        (3, '3 Days'),
        (7, '7 Days'),
        (15, '15 Days'),
        (30, '30 Days'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    plan_days = models.IntegerField(choices=PLAN_CHOICES)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer.name} - {self.start_date} to {self.end_date}"

class Order(models.Model):
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    BOTH = 'Both'
    MEAL_CHOICES = [
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
        (BOTH, 'Both')
    ]
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subscription.customer.name} - {self.meal_type} on {self.date}"
