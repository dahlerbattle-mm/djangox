# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('dashboard/summary/', TemplateView.as_view(template_name='dashboards/summary.html'), name='summary'),
    path('dashboard/revenue/', TemplateView.as_view(template_name='dashboards/revenue.html'), name='revenue'),
    path('dashboard/expenses/', TemplateView.as_view(template_name='dashboards/expenses.html'), name='expenses'),
    path('dashboard/financials/', TemplateView.as_view(template_name='dashboards/financials.html'), name='financials'),
    path('dashboard/saas_metrics/', TemplateView.as_view(template_name='dashboards/saas_metrics.html'), name='saas_metrics'),
    path('dashboard/pipeline/', TemplateView.as_view(template_name='dashboards/pipeline.html'), name='pipeline'),
    path('dashboard/product/', TemplateView.as_view(template_name='dashboards/product.html'), name='product'),
    path('dashboard/services/', TemplateView.as_view(template_name='dashboards/services.html'), name='services'),
]
