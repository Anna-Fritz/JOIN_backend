# Generated by Django 5.1.6 on 2025-03-08 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management_app', '0009_auto_20250308_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(default='#000000', max_length=7),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
