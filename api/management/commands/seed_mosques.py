from django.core.management.base import BaseCommand
from api.models import Mosque


MOSQUES = [
    {
        "name": "Chowk Masjid",
        "address": "Chowk Area, Pernambut, Vellore District, TN",
        "latitude": 12.9265,
        "longitude": 78.9270,
    },
    {
        "name": "Jamiya Masjid (Jamia Mosque)",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9270,
        "longitude": 78.9265,
    },
    {
        "name": "Nawab Daryakhan Masjid",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9258,
        "longitude": 78.9280,
    },
    {
        "name": "Rasheedabad Masjid",
        "address": "Rasheedabad, Pernambut, Vellore District, TN",
        "latitude": 12.9245,
        "longitude": 78.9255,
    },
    {
        "name": "Masjid-e-Fazal",
        "address": "Near Pernambut, Vellore District, TN",
        "latitude": 12.9280,
        "longitude": 78.9290,
    },
    {
        "name": "Lal Masjid",
        "address": "Lal Mosque Street, Pernambut, Vellore District, TN",
        "latitude": 12.9262,
        "longitude": 78.9268,
    },
    {
        "name": "Madina Masjid",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9275,
        "longitude": 78.9260,
    },
    {
        "name": "Masjid-e-Huda (Dawat-ul-Quran)",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9250,
        "longitude": 78.9275,
    },
    {
        "name": "Park Masjid",
        "address": "Park Area, Pernambut, Vellore District, TN",
        "latitude": 12.9268,
        "longitude": 78.9285,
    },
    {
        "name": "Road Masjid-e-Ahle Hadees",
        "address": "Main Road, Pernambut, Vellore District, TN",
        "latitude": 12.9255,
        "longitude": 78.9262,
    },
    {
        "name": "New Masjid-e-Ahle Hadees",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9272,
        "longitude": 78.9272,
    },
    {
        "name": "Small Masjid-e-Ahle Hadees",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9260,
        "longitude": 78.9278,
    },
    {
        "name": "Masjid-e-Istiqamath",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9248,
        "longitude": 78.9265,
    },
    {
        "name": "Ahle Hadees Forquan Masjid",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9278,
        "longitude": 78.9255,
    },
    {
        "name": "Masjid-e-Hassaniya Ahle Hadees",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9265,
        "longitude": 78.9295,
    },
    {
        "name": "Ahle Hadees Jamiya Masjid",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9252,
        "longitude": 78.9270,
    },
    {
        "name": "Masjid-e-Shekul Hadees",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9282,
        "longitude": 78.9260,
    },
    {
        "name": "Masjid Umar (Masjid-E-Umar)",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9258,
        "longitude": 78.9288,
    },
    {
        "name": "Masjid-E-Mohammadia TNTJ Markaz",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9270,
        "longitude": 78.9248,
    },
    {
        "name": "Charminar Complex Masjid",
        "address": "Subbarao Pet, Pernambut, Vellore District, TN",
        "latitude": 12.9242,
        "longitude": 78.9278,
    },
    {
        "name": "Mothi Masjid",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9285,
        "longitude": 78.9268,
    },
    {
        "name": "Masjid-e-Mamur",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9255,
        "longitude": 78.9252,
    },
    {
        "name": "Masjid-e-Deewan",
        "address": "Pernambut, Vellore District, TN",
        "latitude": 12.9275,
        "longitude": 78.9282,
    },
]


class Command(BaseCommand):
    help = "Seed the database with all 23 Pernambut mosques"

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for data in MOSQUES:
            mosque, is_new = Mosque.objects.get_or_create(
                name=data["name"],
                defaults={
                    "address":   data["address"],
                    "latitude":  data["latitude"],
                    "longitude": data["longitude"],
                    # Default prayer times (Pernambut approximate IST)
                    "fajr":    "05:10:00",
                    "dhuhr":   "13:15:00",
                    "asr":     "16:30:00",
                    "maghrib": "18:30:00",
                    "isha":    "19:45:00",
                    "jummah":  "13:00:00",
                },
            )
            if is_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✅  Created: {mosque.name}"))
            else:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"  ⏭️   Skipped (already exists): {mosque.name}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done! {created} mosque(s) created, {skipped} already existed."
        ))
