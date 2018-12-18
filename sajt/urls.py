from django.urls import path

from sajt.views import MyMessages
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("myMessages", MyMessages.as_view(), name="myMessages")
]
