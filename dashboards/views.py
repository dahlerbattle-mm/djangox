from django.shortcuts import render
from django.views.generic import TemplateView

class RevenuePageView(TemplateView):
    template_name = "dashboards/revenue.html"

class SummaryPageView(TemplateView):
    template_name = "dashboards/summary.html"

class ExpensesPageView(TemplateView):
    template_name = "dashboards/expenses.html"

class FinancialsPageView(TemplateView):
    template_name = "dashboards/financials.html"

class SaaSMetricsPageView(TemplateView):
    template_name = "dashboards/saas_metrics.html"

class ServicesPageView(TemplateView):
    template_name = "dashboards/services.html"

class PipelinePageView(TemplateView):
    template_name = "dashboards/pipeline.html"

class ProductPageView(TemplateView):
    template_name = "dashboards/product.html"
