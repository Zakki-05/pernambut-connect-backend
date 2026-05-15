from api.models import Mosque

mosques_data = [
    {
        "name": "Chowk Masjid",
        "address": "Bazaar Street, Pernambut",
        "latitude": 12.9415, "longitude": 78.7122,
        "fajr": "04:55", "dhuhr": "12:30", "asr": "16:45", "maghrib": "18:42", "isha": "20:15", "jummah": "13:30"
    },
    {
        "name": "Jamiya Masjid",
        "address": "Town Center, Pernambut",
        "latitude": 12.9420, "longitude": 78.7130,
        "fajr": "05:00", "dhuhr": "12:45", "asr": "17:00", "maghrib": "18:42", "isha": "20:30", "jummah": "13:15"
    },
    {
        "name": "Road Masjid (Markaz)",
        "address": "Main Highway, Pernambut",
        "latitude": 12.9450, "longitude": 78.7150,
        "fajr": "04:45", "dhuhr": "12:30", "asr": "15:45", "maghrib": "18:42", "isha": "20:00", "jummah": "13:00"
    },
    {
        "name": "Lal Masjid",
        "address": "Old Town, Pernambut",
        "latitude": 12.9400, "longitude": 78.7110,
        "fajr": "05:05", "dhuhr": "13:00", "asr": "17:15", "maghrib": "18:42", "isha": "20:30", "jummah": "13:45"
    },
    {
        "name": "Madina Masjid",
        "address": "Housing Board, Pernambut",
        "latitude": 12.9480, "longitude": 78.7200,
        "fajr": "04:50", "dhuhr": "12:30", "asr": "16:30", "maghrib": "18:42", "isha": "20:15", "jummah": "13:15"
    },
    {
        "name": "Masjid-e-Bilal",
        "address": "Station Road, Pernambut",
        "latitude": 12.9500, "longitude": 78.7250,
        "fajr": "05:00", "dhuhr": "12:45", "asr": "16:45", "maghrib": "18:42", "isha": "20:30", "jummah": "13:30"
    },
    {
        "name": "Makka Masjid",
        "address": "New Colony, Pernambut",
        "latitude": 12.9350, "longitude": 78.7050,
        "fajr": "04:55", "dhuhr": "12:30", "asr": "16:45", "maghrib": "18:42", "isha": "20:15", "jummah": "13:15"
    },
    {
        "name": "Masjid-e-Noor",
        "address": "Hospital Road, Pernambut",
        "latitude": 12.9430, "longitude": 78.7140,
        "fajr": "05:00", "dhuhr": "12:45", "asr": "17:00", "maghrib": "18:42", "isha": "20:30", "jummah": "13:15"
    }
]

for m in mosques_data:
    obj, created = Mosque.objects.update_or_create(
        name=m['name'],
        defaults={
            "address": m['address'],
            "latitude": m['latitude'],
            "longitude": m['longitude'],
            "fajr": m['fajr'],
            "dhuhr": m['dhuhr'],
            "asr": m['asr'],
            "maghrib": m['maghrib'],
            "isha": m['isha'],
            "jummah": m['jummah']
        }
    )
    if created:
        print(f"Created: {m['name']}")
    else:
        print(f"Updated: {m['name']}")

print("Successfully populated Pernambut Masjids with perfect timings.")
