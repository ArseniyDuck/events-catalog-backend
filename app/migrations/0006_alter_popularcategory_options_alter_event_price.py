# Generated by Django 4.0 on 2021-12-23 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_event_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='popularcategory',
            options={'verbose_name_plural': 'popular categories'},
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]