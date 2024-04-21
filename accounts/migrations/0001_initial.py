# Generated by Django 5.0.4 on 2024-04-21 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('invite_code', models.CharField(max_length=6, unique=True)),
                ('verification_code_hash', models.CharField(blank=True, max_length=128, null=True)),
                ('code_sent_time', models.DateTimeField(blank=True, null=True)),
                ('referrer_code', models.CharField(blank=True, max_length=6, null=True)),
                ('invited_users', models.ManyToManyField(related_name='referrers', to='accounts.user')),
            ],
        ),
    ]
