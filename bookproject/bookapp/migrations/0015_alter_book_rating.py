# Generated by Django 4.2.6 on 2024-03-16 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0014_book_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.CharField(default='null', max_length=255),
        ),
    ]
