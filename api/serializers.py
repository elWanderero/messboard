from rest_framework import serializers

from base.models import Message, User


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    createdbyName = serializers.CharField(source="author")

    class Meta:
        model = Message
        # fields = "__all__"
        fields = (
            "url",
            "id",
            "author",
            "createdbyName",
            "text",
            "date_created",
            "date_updated",
        )
        extra_kwargs = {"author": {"lookup_field": "username"}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("url", "id", "username", "date_joined", "email")
        extra_kwargs = {"url": {"lookup_field": "username"}}
