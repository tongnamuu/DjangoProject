from django.urls import path, re_path
from . import views

app_name = "users"
urlpatterns = [path("login/", views.LoginView.as_view(), name="login")]

