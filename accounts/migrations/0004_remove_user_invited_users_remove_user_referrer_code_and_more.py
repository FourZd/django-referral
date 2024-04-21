# Generated by Django 5.0.4 on 2024-04-21 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_groups_user_is_superuser_user_last_login_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='invited_users',
        ),
        migrations.RemoveField(
            model_name='user',
            name='referrer_code',
        ),
        migrations.AddField(
            model_name='user',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
