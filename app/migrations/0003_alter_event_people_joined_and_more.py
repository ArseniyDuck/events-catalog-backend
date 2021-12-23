# Generated by Django 4.0 on 2021-12-23 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_category_color_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='people_joined',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='people_required',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
    ]
