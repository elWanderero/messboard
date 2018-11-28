from base.models import Message, User
from rest_framework import serializers


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    createdbyName = serializers.CharField(source="createdby")

    class Meta:
        model = Message
        # fields = "__all__"
        fields = (
            "url",
            "id",
            "createdby",
            "createdbyName",
            "text",
            "created",
            "updated",
        )
        extra_kwargs = {"createdby": {"lookup_field": "name"}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("url", "id", "name", "created", "email")
        extra_kwargs = {"url": {"lookup_field": "name"}}
