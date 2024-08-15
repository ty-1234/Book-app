from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from bookapp.models import Book
from django.utils import timezone
import math




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    user_xp_total = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    progress_percentage_next_level = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    total_pages_read = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    reading_reminder_time = models.TimeField(null=True, blank=True)
    reading_reminder_frequency = models.CharField(max_length=50, null=True, blank=True)
    books_read = models.PositiveIntegerField(default=0)  # New field to track the number of books read
    def __str__(self):
        return self.user.username


    def required_xp_for_next_level(self):
        """
        Calculates the XP required for the next level.
        """
        base_xp = 1000
        xp_increase_per_level = 1000  # Additional XP needed per level beyond the first
        return base_xp + xp_increase_per_level * (self.level - 1)

        
    def update_total_xp_and_level(self):
            """
            Updates the user's total XP based on the xp_earned from all books in the UserBook model.
            Optionally adds additional XP (for new actions) and checks if the user should level up.
            Logs the XP update with a timestamp if the total XP changes.
            """
            # Calculate the new total XP including any added XP.
            user_books = UserBook.objects.filter(user_profile=self)
            new_total_xp = user_books.aggregate(sum_xp=models.Sum('xp_earned'))['sum_xp'] or 0  # Correct aggregation on filtered QuerySet
            
            """
            does the level really have to be reset to 1 every time user updates page?
            yes because if the user inputs a high page number by accident, then level will be permanently stuck at a high level until the
            user reads enough pages to level up again. This is not ideal.
            """

            self.level = 1 
            
            # Check if there's a change in XP to decide if we need to update and log.
            if new_total_xp != self.user_xp_total:
                self.user_xp_total = new_total_xp
                self.total_pages_read = self.user_xp_total / 17  # 17 XP per page

                # level up logic  -> works because levelling is linear
                # the thresholds for each level are every 1000 XP             
                xp_left = self.required_xp_for_next_level() - self.user_xp_total
                
                while xp_left < 0:
                    self.level += 1
                    xp_left = self.required_xp_for_next_level() - self.user_xp_total
                
                # after the loop the xp will be greater than 0
                # so we can calculate the progress percentage, to understand better use the example below
                # example: user has 1800xp in total. -> use this number at the start of this method to calculate the progress percentage
                
                # used for the progress bar in the profile_detail page
                self.progress_percentage_next_level = (((1000 - xp_left) / 1000) * 100)

                self.save()

                # Log this update
                XPUpdateLog.objects.create(user_profile=self, xp_earned=new_total_xp)


# For uniqueness, we use the UserBook model to store the pages read and XP earned for each user and their own version of a book.
class UserBook(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_book_profile")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_book_book")
    pages_read = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    xp_earned = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    class Meta:
        unique_together = ('user_profile', 'book')  # Ensures uniqueness

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.book.title} - Pages Read: {self.pages_read}"



class XPUpdateLog(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="xp_updates")
    xp_earned = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_profile.user.username} - XP: {self.xp_earned} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

class Badge(models.Model):
    label = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', null=True, blank=True)

    def __str__(self):
        return self.label


class AwardedBadge(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_badges')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='awarded_badges')
    awarded_date = models.DateField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.badge.label} - Awarded on: {self.awarded_date}"  
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  
