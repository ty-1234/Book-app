# tasks.py
from datetime import datetime
from celery import shared_task
from .models import UserProfile
from .consumer import NotificationConsumer
from asgiref.sync import async_to_sync

@shared_task
def send_reading_reminders():
    now = datetime.now()
    users = UserProfile.objects.filter(
        reading_reminder_time__hour=now.hour,
        reading_reminder_time__minute=now.minute
    )
    for user in users:
        group_name = f'user_{user.id}'
        message = "Don't forget to continue your reading!"
        NotificationConsumer.send_reading_reminder(group_name, message)


@shared_task
def update_user_statistics(user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    user_profile.update_total_xp_and_level()
    # Add more statistical updates here

@shared_task
def analyze_reading_patterns():
    # Logic to analyze reading patterns
    pass
