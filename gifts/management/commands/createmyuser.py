from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from elizabethandgeorge.settings import SUPERUSER_USERNAME, SUPERUSER_PASSWORD, SUPERUSER_EMAIL


#Used to create a superuser
class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(SUPERUSER_USERNAME,SUPERUSER_EMAIL,SUPERUSER_PASSWORD)