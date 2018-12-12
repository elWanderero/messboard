from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import Message, User


# This can be used to put editable items directly in the admin list view.
# It is enabled by defining functions get_changelist and get_changelist_form
# in the admin that will use it (that would be UserAdmin.)
class UserChangeList(ChangeList):
    def __init__(self, request, model, list_display,
                 list_display_links, list_filter, date_hierarchy,
                 search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin, sortable_by):
        super(UserChangeList, self).__init__(request, model, list_display,
                                             list_display_links, list_filter,
                                             date_hierarchy, search_fields,
                                             list_select_related, list_per_page,
                                             list_max_show_all, list_editable,
                                             model_admin, sortable_by)

        # these need to be defined here, and not in MovieAdmin
        self.list_display = ['action_checkbox', 'username', 'subscriptions']
        self.list_display_links = ['username']
        self.list_editable = ['subscriptions']


# This class is used by the admin view.
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = get_user_model()
    list_display = ('username', 'email', "first_name", "last_name",
                    "is_active", "date_joined", "last_login")

    # This determines what we see in django admin view. Overwrites the
    # one from parent class, but is the same except also has subscriptions
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        ("Subscriptions", {"fields": ("subscriptions",)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )

    # Uncomment below to enable class UserChangeList above.
    # def get_changelist(self, request, **kwargs):
    #     return UserChangeList
    #
    # def get_changelist_form(self, request, **kwargs):
    #     return UserChangeListForm


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "created")


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
