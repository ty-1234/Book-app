# Generated by Django 4.2.6 on 2024-03-14 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0006_book_google_books_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='google_books_id',
        ),
        migrations.AddField(
            model_name='book',
            name='difficulty',
            field=models.IntegerField(default=0, help_text='Difficulty level'),
        ),
    ]
