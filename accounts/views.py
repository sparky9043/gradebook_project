from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .forms import TeacherLoginForm, TeacherCreationForm
from django.urls import reverse_lazy


# Create your views here
class TeacherLoginView(LoginView):
    form_class = TeacherLoginForm
    template_name = "accounts/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_nav"] = True
        context["hide_footer"] = True
        return context


class TeacherLogoutView(LogoutView):
    pass


# def register_view(request):
#     context = {"show_nav": True, "show_footer": True, "show_sticky": True}
#     return render(request, "accounts/register.html", context)
class TeacherRegisterView(CreateView):
    form_class = TeacherCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_nav"] = True
        context["hide_footer"] = True
        return context
