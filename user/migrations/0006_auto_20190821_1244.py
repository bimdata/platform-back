# Generated by Django 2.2.1 on 2019-08-21 12:44
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("user", "0005_auto_20190813_1430")]

    operations = [
        migrations.RenameField(model_name="user", old_name="sub", new_name="legacy_sub"),
        migrations.RunSQL(
            "ALTER INDEX user_user_sub_19c8139f_like RENAME TO user_user_legacy_sub_19c8139f_like"
        ),
        migrations.RemoveField(model_name="user", name="refresh_token"),
    ]
