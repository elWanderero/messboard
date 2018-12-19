from django.urls import path

from . import views

app_name = "sajt"

urlpatterns = [
    path("", views.index, name="index"),
    path("message-list", views.MessageList.as_view(), name="message-list"),
    path("messages/<int:pk>", views.MessageDetail.as_view(), name="message-detail"),
    path("messages/<int:pk>/delete", views.MessageDelete.as_view(), name="message-delete"),
    path("messages/<int:pk>/edit", views.MessageEdit.as_view(), name="message-edit")
]
