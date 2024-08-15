from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    cover_art = models.ImageField(default='static/img/cover_art/default_image.svg')
    author = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.CharField(max_length=255, default="General")
    pages = models.IntegerField(help_text="Number of pages")
    isbn = models.CharField(max_length=255, default="null")
    book_total_xp = models.PositiveBigIntegerField(help_text="XP points", default=0)
    rating  = models.CharField(max_length=255, default="null")    
    
    def __str__(self):
        return self.title
