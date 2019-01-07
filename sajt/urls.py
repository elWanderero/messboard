from django.urls import path

from . import views

app_name = "sajt"

urlpatterns = [
    path("", views.my_subscriptions, name="my-subscriptions"),
    path(
        "users/<str:username>",
        views.UserMessageList.as_view(),
        name="user-message-list",
    ),
    path(
        "users/<str:username>/subscriptions",
        views.my_subscriptions,
        name="subscriptions",
    ),
    path(
        "users/<str:slug>/subscriptions/<str:subscription_username>/add",
        views.AddSubscription.as_view(),
        name="add-subscription",
    ),
    path(
        "users/<str:slug>/subscriptions/<str:subscription_username>/delete",
        views.RemoveSubscription.as_view(),
        name="remove-subscription",
    ),
    path("messages", views.message_list, name="message-list"),
    path("messages/<int:pk>", views.MessageDetail.as_view(), name="message-detail"),
    path(
        "messages/<int:pk>/delete",
        views.MessageDelete.as_view(),
        name="message-delete",
    ),
    path("messages/<int:pk>/edit", views.MessageEdit.as_view(), name="message-edit"),
]
