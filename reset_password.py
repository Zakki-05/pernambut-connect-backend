import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def reset_password(email=None, password=None):
    if not email or not password:
        superusers = User.objects.filter(is_superuser=True)
        if not superusers.exists():
            print("No superusers found.")
            return

        print("Available Superusers:")
        for i, user in enumerate(superusers):
            print(f"{i+1}. {user.email} (Username: {user.username})")
        
        print("\nUsage: python reset_password.py <email> <new_password>")
        return

    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        print(f"Successfully updated password for {email}")
    except User.DoesNotExist:
        print(f"User with email {email} not found.")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        reset_password(sys.argv[1], sys.argv[2])
    else:
        reset_password()
