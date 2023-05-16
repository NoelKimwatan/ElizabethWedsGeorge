from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

#Used to create a superuser
class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ['SUPERUSER_USERNAME']).exists():
            User.objects.create_superuser(os.environ['SUPERUSER_USERNAME'],os.environ['SUPERUSER_EMAIL'],os.environ['SUPERUSER_PASSWORD'])