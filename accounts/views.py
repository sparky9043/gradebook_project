from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    context = { 'show_nav': True, 'show_footer': True }
    return render(request, 'accounts/register.html', context)