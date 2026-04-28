from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# from django.http import HttpResponse


# Create your views here.
def index(request):
    """Display index at main url"""
    context = {"show_nav": True, "show_footer": True, "show_sticky": True}
    return render(request, "core/index.html", context)


# Dashboard view
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("accounts:login_view")
    template_name = "core/dashboard.html"
