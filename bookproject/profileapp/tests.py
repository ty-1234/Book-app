from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, XPUpdateLog, UserBook, Book

class ProfileAppTests(TestCase):

    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # URL for login redirection
        self.login_url = reverse('login')  # Update with the actual name of your login URL

        #Need to setup login redirect 
    """"def test_redirect_if_not_logged_in(self):
        # Attempt to access profile update page without being logged in
        response = self.client.get(reverse('update_profile'))
        self.assertRedirects(response, f'{self.login_url}?next=/profile/update/')""" 

    def test_logged_in_user_access_profile(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Access profile detail page
        response = self.client.get(reverse('profile_detail'))
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_user_profile_creation_on_signup(self):
        # Assert that a UserProfile instance was created for the new user
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())

    def test_update_profile_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Attempt to update the user profile
        response = self.client.post(reverse('update_profile'), {'biography': 'New biography text'})
        # Check redirect to profile detail page after update
        self.assertRedirects(response, reverse('profile_detail'))
        # Fetch the updated user profile
        updated_profile = UserProfile.objects.get(user__username='testuser')
        # Assert the biography was updated correctly
        self.assertEqual(updated_profile.biography, 'New biography text')


class LevelingAndLoggingTests(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create some books with sufficient XP for testing the leveling scheme
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Author 1",
            book_total_xp=3000,  # Adjust XP value as needed
            pages=100  # Ensure to include pages to satisfy NOT NULL constraint
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Author 2",
            book_total_xp=4500,  # Adjust XP value as needed
            pages=150  # Ensure to include pages to satisfy NOT NULL constraint
        )

        # Add books to users and simulate some reading activity
        UserBook.objects.create(user_profile=self.user1.profile, book=self.book1, pages_read=100, xp_earned=3000)  # Adjust XP earned as needed
        UserBook.objects.create(user_profile=self.user2.profile, book=self.book2, pages_read=150, xp_earned=4500)  # Adjust XP earned as needed

    def test_level_up_and_logging(self):
        # Ensure initial level is 1 for a fair test
        self.assertEqual(self.user1.profile.level, 1, "Initial level is not 1.")

        # Trigger the XP and level update process for profile1
        self.user1.profile.update_total_xp_and_level()

        # Assert that the level is higher than 1 after updating XP and leveling up
        self.assertTrue(self.user1.profile.level > 1, "UserProfile did not level up correctly.")

        # Assert that an XPUpdateLog entry is created
        self.assertTrue(XPUpdateLog.objects.filter(user_profile=self.user1.profile).exists(), "XPUpdateLog entry was not created.")