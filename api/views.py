from rest_framework import viewsets
# from rest_framework import generics  # ,status, mixins, permissions
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from base.models import Message, User
from .serializers import MessageSerializer, UserSerializer


# def index(request):
#     return HttpResponse("Hello, world. You're at the API index.")


# Dear myself: Note that with these rest_framwork views,


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer

    lookup_field = "username"


# class MessageList(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer


# class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    This viewset replaces both views above ('list' and 'detail')
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "messages": reverse("message-list", request=request, format=format),
        }
    )
