from django.contrib import admin
from .models import User, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active", "email")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("createdby", "text", "created")


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
