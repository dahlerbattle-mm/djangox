# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('collaboration/gpt_chat/', views.gpt_chat_view, name="gpt_chat"),
    path('collaboration/investor_portal/', views.investor_portal_view, name="smart_model"),
]
