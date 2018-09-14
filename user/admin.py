from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, Notification


@admin.register(User)
class UsersAdmin(UserAdmin):
    fieldsets = (
        ("platform_info", {"fields": ("demo_cloud", "demo_project", "sub")}),
    ) + UserAdmin.fieldsets
