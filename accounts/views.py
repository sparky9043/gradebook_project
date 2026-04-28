from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import TeacherLoginForm
from django.urls import reverse_lazy


# Create your views here
class TeacherLoginView(LoginView):
    form_class = TeacherLoginForm
    template_name = "accounts/login.html"


class TeacherLogoutView(LogoutView):
    pass


def register_view(request):
    context = {"show_nav": True, "show_footer": True, "show_sticky": True}
    return render(request, "accounts/register.html", context)
