from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Initialize Firebase Admin if settings exist
        from django.conf import settings
        import firebase_admin
        from firebase_admin import credentials
        import json

        firebase_key_path = settings.BASE_DIR / 'serviceAccountKey.json'
        firebase_env_key = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

        if firebase_key_path.exists():
            try:
                cred = credentials.Certificate(str(firebase_key_path))
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Firebase init error (file): {e}")
        elif firebase_env_key:
            try:
                service_account_info = json.loads(firebase_env_key)
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Firebase init error (env): {e}")
        else:
            print("Firebase Admin not initialized: No key found.")
