# Generated by Django 4.2.6 on 2024-03-16 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0015_alter_book_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='null', max_length=255),
        ),
    ]
