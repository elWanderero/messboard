from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_safe
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.models import Message, User


# def _user_is_message_owner(view_instance, request):
#     user = request.user
#     author = view_instance.get_object().author
#     return user.is_authenticated and author == user


# Requires a view instance where self.get_object().author exists.
# Adds the requirement that user must be logged in and be identical to the
# self.get_object().author.
class MessageOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        author = self.get_object().author
        return user.is_authenticated and author == user


# Se your starting page, with all your subscriptions.
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

    #     return HttpResponseRedirect(self.get_success_url())


# View ALL messages by ALL users.
def message_list(request):
    template_name = "sajt/message_list.html"
    messages = Message.objects.all()
    one_msg_per_author = (
        messages.distinct("author").only("author").order_by("author")
    )
    messages_by_authors = [
        {
            "author": msg.author.username,
            "messages": messages.filter(author=msg.author).values(
                "text", "date_created"
            ),
        }
        for msg in one_msg_per_author
    ]
    context = {"messages_by_authors": messages_by_authors}
    return render(request, template_name, context)


# View all messages by a user. Each message has a link to view that message
# individually. If logged in as viewed user, present form to post new message.
class UserMessageList(CreateView):
    template_name = "sajt/user_message_list.html"
    # form_class = MessageCreationForm
    fields = ["text"]
    model = Message

    # Dispatch is the outermost function. Here we check if the URL even exists.
    def dispatch(self, request, *args, **kwargs):
        try:
            self.requested_user = User.objects.get(username=self.kwargs["username"])
        except ObjectDoesNotExist:
            raise Http404("Användaren finns inte")
        self.user_is_owner = (
            request.user.is_authenticated and request.user == self.requested_user
        )
        return super().dispatch(request, *args, **kwargs)

    # Check if accessing user is owner of the requested page, and set some
    # context values correspondingly. We set the displayed name and a boolean flag.
    def get_context_data(self, **kwargs):
        self.data = super().get_context_data(**kwargs)
        context = self.data
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

    # URL for successfully submitted new Message form.
    def get_success_url(self):
        return reverse(
            "sajt:user-message-list", kwargs={"username": self.requested_user}
        )

    # from FormMixin
    def form_valid(self, form):
        if not self.user_is_owner:
            return HttpResponseForbidden()
        form.instance.author = self.request.user
        return super().form_valid(form)


# View and, if logged as correct user, provide links to edit and delete that message.
@method_decorator(require_safe, name="dispatch")
class MessageDetail(DetailView):
    template_name = "sajt/message_detail.html"
    model = Message


# If logged as correct user, edit a single message.
class MessageDelete(MessageOwnerRequiredMixin, DeleteView):
    template_name = "sajt/message_delete.html"
    model = Message

    def get_success_url(self):
        return reverse(
            "sajt:user-message-list", kwargs={"username": self.request.user.username}
        )


# If logged as correct user, delete a single message.
class MessageEdit(MessageOwnerRequiredMixin, UpdateView):
    template_name = "sajt/message_edit.html"
    model = Message
    fields = ["text"]

    def get_success_url(self):
        return reverse("sajt:message-detail", kwargs={"pk": self.object.id})
