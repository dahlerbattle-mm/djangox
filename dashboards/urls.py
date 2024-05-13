# urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('dashboard/summary/', views.summary_view, name="summary"),
    path('dashboard/revenue/', views.revenue_view, name="revenue"),
    path('dashboard/expenses/', views.expenses_view, name="expenses"),
    path('dashboard/financials/', views.financials_view, name="financials"),
    path('dashboard/saas_metrics/', views.saas_view, name="saas_metrics"),
    path('dashboard/pipeline/', views.pipeline_view, name="pipeline"),
    path('dashboard/product/', views.product_view, name="product"),
    path('dashboard/services/', views.services_view, name="services"),
    path('dashboard/hr/', views.hr_view, name="hr"),
    path('dashboard/cashflow/', views.cashflow_view, name="cashflow"),
]
