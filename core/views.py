from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    """View of index at home url"""

    template_name = "core/index.html"
