# Generated by Django 4.2.17 on 2025-03-19 16:44
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import migrations
from django.db import models


def check_platform_url_defined(apps, schema_editor):
    if not settings.PLATFORM_URL:
        raise ImproperlyConfigured(
            "Env variable PLATFORM_URL must be defined during migrations"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0015_alter_user_options_user_user_user_email_5f6a77_idx"),
    ]

    operations = [
        migrations.RunPython(check_platform_url_defined),
        migrations.AddField(
            model_name="user",
            name="initial_referer",
            field=models.URLField(
                blank=True, default=settings.PLATFORM_URL, max_length=255, null=True
            ),
        ),
    ]
