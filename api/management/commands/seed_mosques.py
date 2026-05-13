from django.core.management.base import BaseCommand
from api.models import Mosque

class Command(BaseCommand):
    help = 'Seed database with Pernambut mosque data'

    def handle(self, *args, **kwargs):
        mosques = [
            {
                'name': 'Road Masjid',
                'latitude': 12.9430,
                'longitude': 78.6830,
                'address': 'Main Road, Pernambut, Vellore District, TN',
                'fajr': '05:10',
                'dhuhr': '01:30',
                'asr': '04:45',
                'maghrib': '06:15',
                'isha': '08:00',
                'jummah': '12:50',
            },
            {
                'name': 'Nayee Masjid',
                'latitude': 12.9445,
                'longitude': 78.6850,
                'address': 'Nayee Masjid Street, Pernambut, Vellore District, TN',
                'fajr': '05:10',
                'dhuhr': '01:30',
                'asr': '04:45',
                'maghrib': '06:15',
                'isha': '08:00',
                'jummah': '12:45',
            },
            {
                'name': 'Choti Masjid',
                'latitude': 12.9420,
                'longitude': 78.6840,
                'address': 'Choti Masjid Area, Pernambut, Vellore District, TN',
                'fajr': '05:10',
                'dhuhr': '01:30',
                'asr': '04:45',
                'maghrib': '06:15',
                'isha': '08:00',
                'jummah': '12:40',
            },
            {
                'name': 'Masjid e Ihsaan',
                'latitude': 12.9460,
                'longitude': 78.6870,
                'address': 'Ihsaan Nagar, Pernambut, Vellore District, TN',
                'fajr': '05:10',
                'dhuhr': '01:30',
                'asr': '04:45',
                'maghrib': '06:15',
                'isha': '08:00',
                'jummah': '01:00',
            },
        ]

        for data in mosques:
            mosque, created = Mosque.objects.update_or_create(
                name=data['name'],
                defaults=data,
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status}: {mosque.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! {Mosque.objects.count()} mosques in database.'))
