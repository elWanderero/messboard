from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_safe
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.models import Message, User


def _user_is_message_owner(view_instance, request):
    user = request.user
    author = view_instance.get_object().author
    return user.is_authenticated and author == user


class MessageOwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not _user_is_message_owner(self, request):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


@require_safe
@login_required
def index(request) -> HttpResponse:
    subs = request.user.subscriptions.all().only("id", "username")
    messages = Message.objects.filter(author__in=subs).only("text", "date_created")
    messages_by_authors = [
        {
            "author": sub.username,
            "messages": messages.filter(author=sub).values("text", "date_created"),
        }
        for sub in subs
    ]
    context = {"messages_by_authors": messages_by_authors}
    return render(request, "sajt/index.html", context)


class UserMessageList(CreateView):
    template_name = "sajt/message_list.html"
    # form_class = MessageCreationForm
    fields = ["text"]
    model = Message

    def dispatch(self, request, *args, **kwargs):
        try:
            self.requested_user = User.objects.get(username=self.kwargs["username"])
        except ObjectDoesNotExist:
            raise Http404("Användaren finns inte")
        self.user_is_owner = (
            request.user.is_authenticated and request.user == self.requested_user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_list = self.model.objects.filter(author=self.requested_user).defer(
            "author"
        )
        context["message_list"] = message_list
        if self.user_is_owner:
            context["shown_name"] = "Dina"
        else:
            context["shown_name"] = self.kwargs["username"]
        context["user_is_owner"] = self.user_is_owner
        return context

    def get_success_url(self):
        return reverse("sajt:message-list", kwargs={"username": self.requested_user})

    # from FormMixin
    def form_valid(self, form):
        if not self.user_is_owner:
            return HttpResponseForbidden()
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(require_safe, name="dispatch")
class MessageDetail(DetailView):
    template_name = "sajt/message_detail.html"
    model = Message


class MessageDelete(MessageOwnerRequiredMixin, DeleteView):
    template_name = "sajt/message_delete.html"
    model = Message

    def get_success_url(self):
        return reverse(
            "sajt:message-list", kwargs={"username": self.request.user.username}
        )


class MessageEdit(MessageOwnerRequiredMixin, UpdateView):
    template_name = "sajt/message_edit.html"
    model = Message
    fields = ["text"]

    def get_success_url(self):
        return reverse("sajt:message-detail", kwargs={"pk": self.object.id})
