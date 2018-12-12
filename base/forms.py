import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as AuthChangeForm, \
    UserCreationForm as AuthCreationForm

logger = logging.getLogger(__name__)


class UserCreationForm(AuthCreationForm):
    class Meta(AuthCreationForm):
        model = get_user_model()
        fields = ('username', 'email')


class UserChangeForm(AuthChangeForm):
    class Meta(AuthChangeForm):
        model = get_user_model()
        # fields = UserChangeForm.Meta.fields
        fields = ("subscriptions",)
        # fields = UserChangeForm.Meta.fields + "subscriptions")  # ('username', 'email')


class UserChangeListForm(forms.ModelForm):
    subscriptions = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), required=False
    )
