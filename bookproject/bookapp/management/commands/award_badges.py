from django.core.management.base import BaseCommand
from profileapp.views import award_badges

class Command(BaseCommand):
    help = 'Awards badges to users'

    def handle(self, *args, **options):
        award_badges()  # Call without providing a request parameter
        self.stdout.write(self.style.SUCCESS('Badges awarded successfully'))