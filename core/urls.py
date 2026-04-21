from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Core app main paths
    path('', views.index, name="index"),

    # ping path of con-jobs
    path('ping/', views.ping, name="ping"),
]