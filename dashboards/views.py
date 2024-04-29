from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json

# class RevenuePageView(TemplateView):
#     template_name = "dashboards/revenue.html"

def revenue_view(request):
    metrics = settings.REVENUE_CATEGORIES
    return render(request, 'dashboards/revenue.html', {'metrics': metrics})

# class SummaryPageView(TemplateView):
#     template_name = "dashboards/summary.html"

def summary_view(request):
    metrics = settings.SUMMARY_CATEGORIES
    return render(request, 'dashboards/summary.html', {'metrics': metrics})

# class ExpensesPageView(TemplateView):
#     template_name = "dashboards/expenses.html"

def expenses_view(request):
    metrics = settings.EXPENSES_CATEGORIES
    return render(request, 'dashboards/expenses.html', {'metrics': metrics})

# class FinancialsPageView(TemplateView):
#     template_name = "dashboards/financials.html"

def financials_view(request):
    metrics = settings.FINANCIAL_CATEGORIES
    return render(request, 'dashboards/financials.html', {'metrics': metrics})

# class SaaSMetricsPageView(TemplateView):
#     template_name = "dashboards/saas_metrics.html"

def saas_view(request):
    metrics = settings.SAAS_METRICS_CATEGORIES
    return render(request, 'dashboards/saas_metrics.html', {'metrics': metrics})

# class ServicesPageView(TemplateView):
#     template_name = "dashboards/services.html"

def services_view(request):
    metrics = settings.SERVICES_CATEGORIES
    return render(request, 'dashboards/services.html', {'metrics': metrics})

# class PipelinePageView(TemplateView):
#     template_name = "dashboards/pipeline.html"

def pipeline_view(request):
    metrics = settings.PIPELINE_CATEGORIES
    return render(request, 'dashboards/pipeline.html', {'metrics': metrics})

# class ProductPageView(TemplateView):
#     template_name = "dashboards/product.html"

def product_view(request):
    metrics = settings.PRODUCT_CATEGORIES
    return render(request, 'dashboards/product.html', {'metrics': metrics})