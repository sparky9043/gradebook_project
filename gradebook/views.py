from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.


class GradebookHomeView(LoginRequiredMixin, TemplateView):
    template_name = "gradebook/home.html"
    login_url = reverse_lazy("accounts:login_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_nav"] = True
        context["show_footer"] = True
        return context
