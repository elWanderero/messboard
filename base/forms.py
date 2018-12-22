from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as AuthUserChangeForm, \
    UserCreationForm as AuthUserCreationForm


class UserCreationForm(AuthUserCreationForm):
    class Meta(AuthUserCreationForm):
        model = get_user_model()
        fields = AuthUserCreationForm.Meta.fields


class UserChangeForm(AuthUserChangeForm):
    class Meta(AuthUserChangeForm):
        model = get_user_model()
        fields = AuthUserChangeForm.Meta.fields


class UserChangeListForm(forms.ModelForm):
    subscriptions = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(), required=False
    )


# class MessageCreationForm(forms.ModelForm):
#     class Meta(forms.ModelForm):
#         model = Message
#         fields = ["text"]
