# Generated by Django 4.2.8 on 2024-03-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0019_userprofile_reading_reminder_frequency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='awardedbadge',
            name='progress',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
