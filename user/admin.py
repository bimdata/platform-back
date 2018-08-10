from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, Notification

# Register your models here.
@admin.register(User)
class UsersAdmin(UserAdmin):
    fieldsets = (
        ("platform_info", {"fields": ("demo_cloud", "demo_project")}),
    ) + UserAdmin.fieldsets
