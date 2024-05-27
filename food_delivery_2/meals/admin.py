from django.contrib import admin
from .models import Customer, SubscriptionPlan, MealOff, OrderStatistics


class OrderStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'lunch_basic', 'lunch_premium', 'dinner_basic', 'dinner_premium']
    readonly_fields = ['date', 'lunch_basic', 'lunch_premium', 'dinner_basic', 'dinner_premium']

admin.site.register(OrderStatistics, OrderStatisticsAdmin)



admin.site.register(Customer)
admin.site.register(SubscriptionPlan)
admin.site.register(MealOff)
