# Generated by Django 4.2.1 on 2023-05-22 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0007_customuser_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
