# Generated by Django 2.2.1 on 2019-08-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_auto_20181003_1154"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="refresh_token",
            field=models.TextField(blank=True, null=True, verbose_name="Refresh Token"),
        ),
    ]
