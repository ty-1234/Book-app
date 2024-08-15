from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseRedirect
import requests
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Value
from googleapiclient.discovery import build 
from django.conf import settings
from bookapp.models import Book
from .models import UserBook, UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import BadgeForm
from .models import Badge,AwardedBadge
from django.http import JsonResponse
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from .forms import ReminderForm

@login_required
def index_view(request):
    context = {}
    return render(request, 'profile_index.html', context)

@login_required
def profile_detail(request):     
    profile = request.user.profile
    required_xp_for_next_level = profile.required_xp_for_next_level()



    return render(request, 'profile_detail.html', {
        'profile': profile,
        'required_xp_for_next_level': required_xp_for_next_level,
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            if not request.FILES and 'avatar_choice' in form.cleaned_data and form.cleaned_data['avatar_choice']:
                profile.avatar = form.cleaned_data['avatar_choice']
            profile.save()
            return redirect('profile_detail')
    else:
        form = UserProfileForm(instance=request.user.profile, user=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def my_library(request):
    
    user_profile = request.user.profile
    
    user_books = UserBook.objects.filter(user_profile=user_profile)
    
    # Pass the books to the template
    return render(request, 'books_list.html', context={'user_books': user_books})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_book_to_library(request):
    data = json.loads(request.body)
    user_profile = request.user.profile

    # Attempt to get or create the book instance without book_total_xp
    book, _ = Book.objects.get_or_create(
        title=data['title'],
        defaults={'cover_art': data['cover_art'], 'categories': data['categories'],
                  'author': data['author'], 'pages': data['pages'],
                  'isbn': data['isbn'], 'description': data['description'], 'rating': data['rating']}
    )
    
    if book.rating == "":
        book.rating = "null"
        book.save()
        
    if book.isbn == '':
        book.isbn = "null"
        book.save()

    book.book_total_xp = int(data['pages']) * 17  # Ensure pages is an int
    book.save()  # Don't forget to save the book object after modification

    # Add the book to the user's library through user_books for uniqueness -> for each UserProfile to have their own version of a book
    user_book, _ = UserBook.objects.get_or_create(
        user_profile=user_profile,
        book=book,
        defaults={'pages_read': 0, 'xp_earned': 0}
        )

    return JsonResponse({'status': 'success', 'message': 'Book added successfully'})


def read_book(request, book_id, isbn):
    user_profile = request.user.profile
    # UserBook.objects.filter(user_profile=user_profile, book_id=book_id).delete()
    #return HttpResponseRedirect(reverse_lazy('my_library'))
    context = {
        'book_id': book_id,
        'isbn': isbn,
        # Include other necessary context variables here
    }
    return render(request, "read_book.html", context)

def send_notes(request):
    if request.method == "POST":
        notes = request.POST.get("notes")
        email = request.user.email

        try:
            send_mail(
                subject = "Here are your notes from EchoPages!",
                message = notes,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently=False,
            )
            print("\nEmail has been sent: ", email)

        except Exception as e:
            print("\n", e)
        
        # return render(request, "read_book.html")        
        return HttpResponseRedirect(reverse('read_book', args=[request.POST.get("book_id"), request.POST.get("isbn")]))
          



def remove_book_from_library(request, book_id):
    user_profile = request.user.profile
    UserBook.objects.filter(user_profile=user_profile, book_id=book_id).delete()
    return HttpResponseRedirect(reverse_lazy('my_library'))

def confirm_remove_book(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'confirm_remove_book.html', {'book': book})

@require_POST
def update_current_page(request):
    data = json.loads(request.body)
    book_id = data.get('bookId')
    current_page = data.get('currentPage')

    user_profile = request.user.profile
    book = get_object_or_404(Book, id=book_id)
    
    # 'get' the user_book instance for the current user and book -> it will be there since it's already in the library
    user_book = UserBook.objects.get(user_profile=user_profile, book=book)

    # This is further validation to ensure that the current page doesn't exceed the total pages of the book
    current_page = min(current_page, book.pages)
    
    # Assuming 17 XP per page read
    new_xp_earned = current_page * 17  # Adjust this logic as needed for XP calculation

    user_book.pages_read = current_page
    user_book.xp_earned = new_xp_earned
    user_book.save()
    
    user_profile.update_total_xp_and_level() # Update the user's total XP and level
    user_profile.books_read = user_profile.user_book_profile.count()  # Update books_read based on the number of UserBook instances
    return JsonResponse({'message': f'Progress saved successfully!, Total XP earned from book: {user_book.xp_earned}', 'xpEarned': user_book.xp_earned})

@login_required
def xp_progress_data(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    updates = user_profile.xp_updates.all().order_by('timestamp')

    data = {
        'labels': [update.timestamp.strftime('%Y-%m-%d %H:%M') for update in updates],
        'datasets': [{
            'label': 'XP Progress',
            'data': [update.xp_earned for update in updates],
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1,
        }]
    }
    return JsonResponse(data)


def award_badges():
    # Implement logic to award badges based on certain criteria
    # For example, loop through all user profiles and update badge progress
    all_users = UserProfile.objects.all() 
   
    for user_profile in all_users:
        
        # Example criteria for updating badge progress
        if user_profile.level >= 5:
            # Check if the user qualifies for the 'Level 5 Master' badge
            badge, _ = Badge.objects.get_or_create(label='Level 5 Master', defaults={'description': 'Awarded for reaching level 5'})
            awarded_badge, created = AwardedBadge.objects.get_or_create(badge=badge, user_profile=user_profile)
            if created:
                awarded_badge.progress = 100  # Set initial progress to 100% since the criteria is met
            awarded_badge.save()   
        if user_profile.books_read >= 10:  # Adjust the number of books as desired
            badge, _ = Badge.objects.get_or_create(label='Bookworm', defaults={'description': 'Awarded for reading 10 books'})
            awarded_badge, created = AwardedBadge.objects.get_or_create(badge=badge, user_profile=user_profile)
            if created:
                awarded_badge.progress = 100  # Set initial progress to 100% since the criteria is met
            awarded_badge.save()
        if user_profile.user_xp_total >= 30000:
            badge, _ = Badge.objects.get_or_create(label='Legendary', defaults={'description': 'Awarded for earning 30000 total points'})
            awarded_badge, created = AwardedBadge.objects.get_or_create(badge=badge, user_profile=user_profile)
            if created:
                awarded_badge.progress = 100
            awarded_badge.save()
        if user_profile.level >= 20:
            # Check if the user qualifies for the 'Level 5 Master' badge
            badge, _ = Badge.objects.get_or_create(label='Level 20 champion', defaults={'description': 'Awarded for reaching level 20'})
            awarded_badge, created = AwardedBadge.objects.get_or_create(badge=badge, user_profile=user_profile)
            if created:
                awarded_badge.progress = 100  # Set initial progress to 100% since the criteria is met
            awarded_badge.save()   
        
    return  

def badges_list(request):
    badges = Badge.objects.all()
    return render(request, 'badge/badges_list.html', {'badges': badges})

def create_badge(request):
    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('badges_list')
    else:
        form = BadgeForm()
    return render(request, 'badge/badge_form.html', {'form': form})

def view_badge_detail(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return render(request, 'badge/badges_detail.html', {'badge': badge})

def edit_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('badges_list')
    else:
        form = BadgeForm(instance=badge)
    return render(request, 'badge/badge_form.html', {'form': form, 'badge': badge})

def delete_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    if request.method == 'POST':
        badge.delete()
        return redirect('badges_list')
    return render(request, 'badge/badge_confirm_delete.html', {'badge': badge}) 
def send_notification(request):
    message = request.POST.get('message', '')  # Assuming message is sent via POST request
    if message:
        # Create a notification
        Notification.objects.create(user=request.user, message=message)

        # Send notification to WebSocket consumers
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notification_group', {
                'type': 'notification_message',
                'message': message
            }
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
def notification_list(request):
    notifications = Notification.objects.all()  # Fetch all notifications from the database
    return render(request, 'notification_list.html', {'notifications': notifications})



@login_required
def manage_reminders(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('manage_reminders')
    else:
        form = ReminderForm(instance=profile)

    return render(request, 'manage_reminders.html', {'form': form})  
@login_required
def user_awarded_badges(request):
    # Call award_badges to ensure badges are awarded before rendering the page
    award_badges()

    user_profile = request.user.profile

    awarded_badges = user_profile.awarded_badges.all()
    # Print the awarded badges for debugging purposes
   
    return render(request, 'badge/user_awarded_badges.html', {'awarded_badges': awarded_badges})
@login_required
def leaderboard(request):
    leaderboard_data = UserProfile.objects.annotate(
        total_points=Coalesce(('user_xp_total'), Value(0))
    ).order_by('-total_points', '-level').values(
        'user__username', 'level', 'total_points',
    )

    return render(request, 'leaderboard.html', {'leaderboard_data': leaderboard_data}) 
