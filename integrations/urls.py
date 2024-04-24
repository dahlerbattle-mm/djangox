# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('integrations/home/', TemplateView.as_view(template_name='integrations/home.html'), name='integrations'),

]
