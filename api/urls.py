from django.urls import path

# from . import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.conf.urls import include
from . import views

schema_view = get_schema_view(title="messboard API")

router = routers.DefaultRouter()
router.register("messages", views.MessageViewSet)
router.register("users", views.UserViewSet)


# message_list = MessageViewSet.as_view({"get": "list", "post": "create"})

# message_detail = MessageViewSet.as_view(
#     {
#         "get": "retrieve",
#         "put": "update",
#         "patch": "partial_update",
#         "delete": "destroy",
#     }
# )

# user_list = UserViewSet.as_view({"get": "list"})
# user_detail = UserViewSet.as_view({"get": "retrieve"})


# API endpoints
# urlpatterns = format_suffix_patterns(
#     [
#         path("", views.api_root),
#         path("messages/", message_list, name="message-list"),
#         path("messages/<int:pk>/", message_detail, name="message-detail"),
#         path("users/", user_list, name="user-list"),
#         path("users/<int:pk>/", user_detail, name="user-detail"),
#     ]
# )


# Since we're using rest-framework built-in viewSets we can use router
# classes to automatically configure default RESTfull URL endpoints.
urlpatterns = [path("", include(router.urls)), path("schema/", schema_view)]
