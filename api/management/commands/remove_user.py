from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Remove specific user by phone number'

    def handle(self, *args, **kwargs):
        phone = '9342954510'
        deleted_count, _ = User.objects.filter(phone_number=phone).delete()
        if deleted_count:
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted user with phone {phone}'))
        else:
            self.stdout.write(self.style.WARNING(f'No user found with phone {phone}'))
