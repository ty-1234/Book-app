from django.core.management.base import BaseCommand
from django.conf import settings
from os.path import join
from profileapp.models import Badge

class Command(BaseCommand):
    help = 'Seeds the database with initial badge data'

    def handle(self, *args, **kwargs):
        # Create badges and save them to the database
        badges_data = [
            {'label': 'Bookworm', 'description': 'Awarded for reading 10 or more books', 'image': 'bookworm-badge-upscaled.jpg'},
            {'label': 'Level 5 Master', 'description': 'Awarded for reaching level 5', 'image': 'award-151151.svg'},
            {'label': 'Reading Enthusiast', 'description': 'Awarded for reading 25 books', 'image': 'transparent_2024-03-21T14-53-59.png'},
            {'label': 'Legendary', 'description': 'Awarded for earning 30000 total points' , 'image': 'pixel-badge-coin-diamond-flame-shiny-reward-legendary-unique-epic.png'},
            {'label': 'Level 20 Champion', 'description': 'Awarded for reaching level 20', 'image': 'elegant-badge-isolated_23-2150997696.jpg'},
            # Add more badges as needed
        ]
        for badge_data in badges_data:
            image_path = join(settings.MEDIA_ROOT, 'badges', badge_data['image'])
            badge = Badge(label=badge_data['label'], description=badge_data['description'], image=image_path)
            badge.save()
