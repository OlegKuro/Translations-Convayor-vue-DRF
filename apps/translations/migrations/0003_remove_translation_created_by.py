# Generated by Django 3.2.4 on 2021-08-16 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0002_auto_20210816_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='created_by',
        ),
    ]
