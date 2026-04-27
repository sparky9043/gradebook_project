from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import TeacherCreationForm


# Create your views here.
# def login_view(request):
#     return render(request, 'accounts/login.html')
class TeacherLoginView(LoginView):
    # form_class = TeacherCreationForm
    template_name = "accounts/login.html"


def register_view(request):
    context = {"show_nav": True, "show_footer": True, "show_sticky": True}
    return render(request, "accounts/register.html", context)
