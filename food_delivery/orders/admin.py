from django.contrib import admin
from .models import Customer, Subscription, Order

admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Order)
