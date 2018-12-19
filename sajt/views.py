from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_safe
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.models import Message


def _user_is_message_owner(view_instance):
    user = view_instance.request.user
    author = view_instance.get_object().author
    return user.is_authenticated and author == user



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


class MessageList(LoginRequiredMixin, CreateView):
    template_name = "sajt/message_list.html"
    # form_class = MessageCreationForm
    fields = ["text"]
    model = Message
    success_url = reverse_lazy("sajt:message-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_list = self.model.objects.filter(author=self.request.user).defer(
            "author")
        context["message_list"] = message_list
        return context

    # from FormMixin
    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        form.instance.author = self.request.user
        return super().form_valid(form)


class MessageDetail(DetailView):
    template_name = "sajt/message_detail.html"
    model = Message


class MessageDelete(LoginRequiredMixin, DeleteView):
    template_name = "sajt/message_delete.html"
    model = Message
    success_url = reverse_lazy("sajt:message-list")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["short_description"] = self.get_object().__str__()
    #     print(self.get_object().__str__())
    #     return context

    def delete(self, request, *args, **kwargs):
        if _user_is_message_owner(self):
            return super().delete(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if _user_is_message_owner(self):
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class MessageEdit(LoginRequiredMixin, UpdateView):
    template_name = "sajt/message_edit.html"
    model = Message
    fields = ["text"]
    # success_url = reverse_lazy("sajt:message-list", kwargs={"id": })

    def get_success_url(self):
        return reverse_lazy("sajt:message-detail", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        if _user_is_message_owner(self):
            return super().post(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if _user_is_message_owner(self):
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


#####################################################################
# CBV methods that I want to keep around for a while as reference:  #
#####################################################################
# @method_decorator(require_safe, name="dispatch")

# def post(self, request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return HttpResponseForbidden()
#     self.object = self.get_object()
#     return super().post(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     # ex ListView. The result will have key message_list in context.
#     object_list = self.model.objects.filter(author=self.request.user).defer(
#         "author").order_by("date_created")
#
#     context = self.get_context_data(object_list=object_list, form=self.form_class)
#     return render(request, self.template_name, context)

# def post(self, request, *args, **kwargs):
#     return self.get(request, *args, **kwargs)
