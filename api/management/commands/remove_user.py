from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Remove specific user by email'

    def handle(self, *args, **kwargs):
        email = 'test@example.com'
        deleted_count, _ = User.objects.filter(email=email).delete()
        if deleted_count:
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted user with email {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'No user found with email {email}'))
