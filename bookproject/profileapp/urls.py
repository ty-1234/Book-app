from django.urls import path
from . import views

urlpatterns = [
    # /profile
    path('profile-page', views.index_view, name='profile_index'), 
    # /profile/my-library
    path("my-library/", views.my_library, name="my_library"),
    # /profile/update
    path('update/', views.update_profile, name='update_profile'),  
    # /profile/detail
    path('detail/', views.profile_detail, name='profile_detail'),  
    path('add_book_to_library/', views.add_book_to_library, name='add_book_to_library'),
    path('confirm-remove-book/<int:book_id>/', views.confirm_remove_book, name='confirm_remove_book'),
    path('update_current_page/', views.update_current_page, name='update_current_page'),
    path('progress-chart-data/', views.xp_progress_data, name='xp_progress_data'),
    path('read-book/<int:book_id>/<isbn>', views.read_book, name='read_book'),
    path('remove-book-from-library/<int:book_id>/', views.remove_book_from_library, name='remove_book_from_library'),
    path('remove-book-from-library/<int:book_id>/', views.remove_book_from_library, name='remove_book_from_library'),
    path('badges/', views.badges_list, name='badges_list'),
    path('badges/create/', views.create_badge, name='create_badge'),
    path('badges/<int:badge_id>/', views.view_badge_detail, name='view_badge_detail'),
    path('badges/<int:badge_id>/edit/', views.edit_badge, name='edit_badge'),
    path('badges/<int:badge_id>/delete/', views.delete_badge, name='delete_badge'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('badges/awarded/', views.user_awarded_badges, name='user_awarded_badges'),
    path('leaderboard/', views.leaderboard, name='leaderboard')
]
