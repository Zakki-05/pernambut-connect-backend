import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def reset_zakki_password(new_password):
    email = 'zakkiadnan05@gmail.com'
    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"Successfully updated password for {email} and ensured admin status.")
    except User.DoesNotExist:
        print(f"User with email {email} not found. Creating new superuser...")
        User.objects.create_superuser(username='zakki', email=email, password=new_password)
        print(f"Successfully created superuser: {email}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        reset_zakki_password(sys.argv[1])
    else:
        print("Usage: python reset_zakki.py <new_password>")
