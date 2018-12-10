from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("myMessages", views.my_messages, name="myMessages")
]
