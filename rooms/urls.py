from django.urls import path, re_path
from . import views

app_name = "rooms"

urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]

