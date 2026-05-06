from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .forms import TeacherLoginForm, TeacherCreationForm
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here
class TeacherLoginView(LoginView):
    form_class = TeacherLoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Invalid Username or Password")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_nav"] = True
        context["hide_footer"] = True
        return context


class TeacherLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Logout Successful")
        return response


class TeacherRegisterView(CreateView):
    form_class = TeacherCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_nav"] = True
        context["hide_footer"] = True
        return context
