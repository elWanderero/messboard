from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_safe
from django.views.generic.edit import CreateView

from base.models import Message


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


class MyMessages(LoginRequiredMixin, CreateView):
    template_name = "sajt/message_list.html"
    # form_class = MessageCreationForm
    fields = ["text"]
    model = Message
    success_url = "myMessages"

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
