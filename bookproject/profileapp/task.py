from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from .models import UserProfile
from django.contrib.auth.models import User

@shared_task
def send_registration_confirmation_email(user_id):
    # Retrieve the user object
    user = User.objects.get(pk=user_id)
    
    # Prepare email content
    subject = 'Welcome to EchoPages!'
    message = 'Thank you for registering on EchoPages. We hope you enjoy your reading journey!'
    sender_email = settings.EMAIL_HOST_USER  # Update with your sender email
    recipient_list = [user.email]
    html_message = render_to_string('registration_confirmation_email.html')
    
    # Send the email
    send_mail(subject, message, sender_email, recipient_list, html_message=html_message)

@shared_task
def send_weekly_challenge_reminder_email():
    # Get users who need to receive the weekly challenge reminder email
    users = UserProfile.objects.filter(receive_weekly_challenge_reminder=True)
    
    for user_profile in users:
        user_email = user_profile.user.email
        challenge_title = "Weekly Reading Challenge"  # Replace with actual challenge title
        subject = 'Weekly Reading Challenge Reminder'
        message = f'Hi {user_profile.user.username}! Just a friendly reminder about our weekly reading challenge: {challenge_title}. Don\'t forget to participate and earn exciting rewards!'
        sender_email = 'your@example.com'  # Update with your sender email
        recipient_list = [user_email]
        html_message = render_to_string('weekly_challenge_reminder_email.html', {'challenge_title': challenge_title})
        
        # Send the email
        send_mail(subject, message, sender_email, recipient_list, html_message=html_message)

@shared_task
def send_inactive_user_reminder_email():
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30))  # Example: users inactive for 30 days
    for user in inactive_users:
        user_email = user.email
        
        subject = 'We Miss You! Come Back to EchoPages'
        message = 'Hi there! We noticed you haven\'t been active on YourApp lately. We miss seeing you around! Don\'t forget to dive back into your reading adventures.'
        sender_email = 'your@example.com'  # Update with your sender email
        recipient_list = [user_email]
        html_message = render_to_string('inactive_user_reminder_email.html')
        
        # Send the email
        send_mail(subject, message, sender_email, recipient_list, html_message)