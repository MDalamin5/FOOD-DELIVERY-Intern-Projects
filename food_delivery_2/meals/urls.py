


from django.urls import path
from .views import home, user_logout, signup, user_login, meal_off, meal_off_success, subscribe, consume_meal, subscription_success, consume_meal_success, invalid_meal_time, order_statistics_view

urlpatterns = [
    path('', home, name='home'),
    path('admin/order-statistics/', order_statistics_view, name='order_statistics'),
    path('meal_off/', meal_off, name='meal_off'),
    path('meal_off/success/', meal_off_success, name='meal_off_success'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('meal_off/', meal_off, name='meal_off'),
    path('meal_off/success/', meal_off_success, name='meal_off_success'),
    path('subscribe/<int:plan_id>/', subscribe, name='subscribe'),
    path('consume_meal/<str:meal_type>/', consume_meal, name='consume_meal'),
    path('subscription_success/', subscription_success, name='subscription_success'),
    path('consume_meal_success/', consume_meal_success, name='consume_meal_success'),
    path('invalid_meal_time/', invalid_meal_time, name='invalid_meal_time'),
]
