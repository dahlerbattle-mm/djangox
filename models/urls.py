# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('models/my_model/', views.my_model_view, name="my_model"),
    path('models/smart_model/', views.smart_model_view, name="smart_model"),
    path('models/datacheck/', views.datacheck_view, name="datacheck"),
]
