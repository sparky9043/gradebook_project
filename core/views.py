from django.shortcuts import render

# from django.http import HttpResponse


# Create your views here.
def index(request):
    """Display index at main url"""
    context = {"show_nav": True, "show_footer": True, "show_sticky": True}
    return render(request, "core/index.html", context)
