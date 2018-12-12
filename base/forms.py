from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as AuthChangeForm, \
    UserCreationForm as AuthCreationForm


class UserCreationForm(AuthCreationForm):
    class Meta(AuthCreationForm):
        model = get_user_model()
        fields = AuthCreationForm.Meta.fields


class UserChangeForm(AuthChangeForm):
    class Meta(AuthChangeForm):
        model = get_user_model()
        fields = AuthChangeForm.Meta.fields


class UserChangeListForm(forms.ModelForm):
    subscriptions = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), required=False
    )
