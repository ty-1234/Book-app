# Generated by Django 4.2.6 on 2024-05-13 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0026_userprofile_session_end_userprofile_session_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='session_end',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='session_start',
        ),
    ]
