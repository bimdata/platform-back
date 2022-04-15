# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, GuidedTour


@admin.register(User)
class UsersAdmin(UserAdmin):
    fieldsets = (
        ("platform_info", {"fields": ("demo_cloud", "demo_project", "sub")}),
    ) + UserAdmin.fieldsets


@admin.register(GuidedTour)
class GuidedTourAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
