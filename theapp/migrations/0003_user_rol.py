# Generated by Django 4.2.1 on 2023-05-21 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0002_remove_ticket_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.CharField(default='usuario', max_length=200),
        ),
    ]
