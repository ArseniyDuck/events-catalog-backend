# Generated by Django 4.0 on 2022-01-05 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_profile_notification_shown',
            field=models.BooleanField(default=True),
        ),
    ]
