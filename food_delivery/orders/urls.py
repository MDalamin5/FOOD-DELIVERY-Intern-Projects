from django.urls import path
from . import views

urlpatterns = [
    path('toggle_meal/<int:subscription_id>/<str:meal_type>/', views.toggle_meal, name='toggle_meal'),
    path('subscription/<int:subscription_id>/', views.subscription_detail, name='subscription_detail'),
]

