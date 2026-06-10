import random
from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Report

# 🔥 Pakai locale Indonesia
fake = Faker('id_ID')


class Command(BaseCommand):
    help = 'Generate fake reports (Indonesia style)'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int, help='Jumlah data yang akan dibuat')

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']

        categories = ['Jalan Rusak', 'Sampah', 'Lampu Mati', 'Drainase', 'Keamanan', 'Pencurian']
        status_choices = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']

        for _ in range(num_records):

            category = random.choice(categories)
            city = fake.city()

            # 🔥 Judul lebih realistis
            title = f"Laporan {category} di {city}"

            # 🔥 Deskripsi lebih natural
            description = f"Terdapat masalah {category.lower()} di wilayah {city}. Mohon segera ditindaklanjuti."

            # 🔥 Lokasi clean (tanpa newline aneh)
            location = fake.address().replace('\n', ', ')

            Report.objects.create(
                title=title,
                category=category,
                description=description,
                location=location,
                status=random.choice(status_choices),
            )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Berhasil membuat {num_records} data laporan!')
        )