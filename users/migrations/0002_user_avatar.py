# Generated by Django 4.1.5 on 2023-01-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.TextField(null=True),
        ),
    ]
