from django.contrib import admin

# Register your models here.

from example.models import PlatformUser


@admin.register(PlatformUser)
class UserAdmin(admin.ModelAdmin):
    """ The OIDC user model admin. """

    list_display = ("sub", "user")
