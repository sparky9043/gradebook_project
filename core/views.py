from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def index(request):
    """Display index at main url"""
    return render(request, "core/index.html")
