# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('subscriptions/', views.subscription_view, name="subscriptions_view"),
]
