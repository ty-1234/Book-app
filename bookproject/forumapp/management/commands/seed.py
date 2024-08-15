from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forumapp.models import Category, Thread, Post
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Seeds the database with initial data for categories, threads, and posts'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, help='Number of each model type to create', default=10)

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))

        # Create categories
        for _ in range(options['number']):
            category = Category.objects.create(
                name=get_random_string(10),  # Example length of 10
                description=get_random_string(50)  # Example length of 50
            )

        # Create threads and posts within each category
        for category in Category.objects.all():
            for _ in range(options['number']):
                thread = Thread.objects.create(
                    title=get_random_string(15),  # Example length of 15
                    posted_by=admin,
                    category=category
                )
                for _ in range(options['number']):
                    Post.objects.create(
                        thread=thread,
                        message=get_random_string(100),  # Example length of 100
                        created_by=admin
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with categories, threads, and posts'))
