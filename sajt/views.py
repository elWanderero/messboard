from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from base.models import Message


@login_required
def index(request) -> HttpResponse:
    subs = request.user.subscriptions.all().only("id", "username")
    messages = Message.objects.filter(author__in=subs).only("text", "created")
    messages_by_authors = [
        {
            "author": sub.username,
            "messages": messages.filter(author=sub).values("text", "created"),
        }
        for sub in subs
    ]
    context = {"messages_by_authors": messages_by_authors}
    return render(request, "sajt/index.html", context)


@login_required
def my_messages(request) -> HttpResponse:
    return HttpResponse("Here you can very clearly see your own messages.")
