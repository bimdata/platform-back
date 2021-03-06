# Generated by Django 2.2.4 on 2019-08-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("user", "0006_auto_20190821_1244")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="legacy_sub",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="sub from BIMData Connect. Kept for backward compatibility",
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Subject identifier",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="sub",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="sub from Keycloak",
                max_length=255,
                null=True,
                unique=True,
            ),
        ),
    ]
