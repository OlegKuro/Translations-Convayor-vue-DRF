# Generated by Django 3.2.4 on 2021-08-15 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]
