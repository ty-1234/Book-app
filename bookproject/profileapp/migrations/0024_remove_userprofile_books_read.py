# Generated by Django 4.2.8 on 2024-04-28 16:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profileapp", "0023_userprofile_books_read"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="books_read",
        ),
    ]
