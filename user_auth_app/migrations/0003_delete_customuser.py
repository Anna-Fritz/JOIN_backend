# Generated by Django 5.1.6 on 2025-02-28 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0002_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
