from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from base.models import Message
from django.shortcuts import render


@login_required
def index(request) -> HttpResponse:
    messages = Message.objects.filter(author=request.user.id).only("text")
    context = {"messages": messages}
    return render(request, "sajt/index.html", context)


@login_required
def my_messages(request) -> HttpResponse:
    return HttpResponse("Here you can very clearly see your own messages.")
