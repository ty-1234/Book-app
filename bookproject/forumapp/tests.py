from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Thread, Post

class ForumTests(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=False)
        self.admin_user = User.objects.create_user(username='adminuser', password='admin12345', is_staff=True)
        # Create a category
        self.category = Category.objects.create(name='General', description='General discussion')

    def test_create_category_by_admin(self):
        self.client.login(username='adminuser', password='admin12345')
        response = self.client.post(reverse('create-category'), {'name': 'New Category', 'description': 'A new category'})
        self.assertEqual(response.status_code, 302)  # Admin creates a category, expecting redirection
        
        self.client.logout()

    def test_create_category_by_non_admin(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create-category'), {'name': 'User Category', 'description': 'A category by user'})
        # Assuming a non-admin user is redirected or forbidden (403), not allowed to create a category
        self.assertTrue(response.status_code in [302, 403], 'Non-admin should not create a category or should be redirected')
        
        self.client.logout()

    def test_create_thread(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('create-thread', kwargs={'category_id': self.category.id}), {'title': 'Test Thread', 'category': self.category.id, 'posted_by': self.user.id})
        self.assertEqual(response.status_code, 302)  # Thread creation redirects to the thread detail or forum index

    def test_create_post(self):
        self.client.login(username='testuser', password='12345')
        thread = Thread.objects.create(title='Initial Thread', posted_by=self.user, category=self.category)
        response = self.client.post(reverse('create-post', kwargs={'thread_id': thread.id}), {'message': 'Test Post', 'thread': thread.id, 'created_by': self.user.id})
        self.assertEqual(response.status_code, 302)  # Post creation redirects to the thread detail

    def test_view_category_detail(self):
        response = self.client.get(reverse('category-detail', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'General discussion')

    def test_view_thread_detail(self):
        thread = Thread.objects.create(title='Test Thread for Viewing', category=self.category, posted_by=self.user)
        response = self.client.get(reverse('thread-detail', kwargs={'thread_id': thread.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, thread.title)

    def test_delete_category_by_admin(self):
        self.client.login(username='adminuser', password='admin12345')
        response = self.client.post(reverse('delete-category', kwargs={'category_id': self.category.id}))
        self.assertEqual(response.status_code, 302)  # Assuming successful deletion redirects

    def test_delete_category_by_non_admin(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete-category', kwargs={'category_id': self.category.id}))
        # Assuming a non-admin user is redirected or receives a 403 Forbidden response
        self.assertTrue(response.status_code in [302, 403], 'Non-admin attempting to delete category should be redirected or forbidden')
