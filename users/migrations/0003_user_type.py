# Generated by Django 4.1.5 on 2023-01-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(default='Client', max_length=25),
        ),
    ]
