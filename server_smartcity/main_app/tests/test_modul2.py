from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from main_app.models import Report


User = get_user_model()


class PrivacyAndDataHidingTests(APITestCase):
    """
    Kelas pengujian untuk modul Visibilitas Data & Privasi Pelapor.

    Menguji mekanisme penyamaran identitas pelapor pada feed publik,
    menampilkan identitas asli pada laporan milik sendiri, serta memastikan
    draf milik pengguna lain tidak dapat dibaca atau dimodifikasi.
    """

    def setUp(self):
        """
        Arrange global:
        Membuat dua user warga dan beberapa data laporan dengan status berbeda.
        """
        self.warga_a = User.objects.create_user(
            username='warga_a',
            password='TestPass123!',
            is_admin=False
        )

        self.warga_b = User.objects.create_user(
            username='warga_b',
            password='TestPass123!',
            is_admin=False
        )

        self.draft_milik_b = Report.objects.create(
            title='Draf Rahasia Warga B',
            category='Infrastruktur',
            description='Ini adalah draf yang belum diajukan.',
            location='Lokasi Rahasia',
            status='DRAFT',
            reporter=self.warga_b,
        )

        self.laporan_publik_a = Report.objects.create(
            title='Jalan Berlubang di Depan Kampus',
            category='Infrastruktur',
            description='Ada lubang besar yang membahayakan pengendara.',
            location='Jl. Soekarno Hatta',
            status='REPORTED',
            reporter=self.warga_a,
        )

        self.laporan_publik_b = Report.objects.create(
            title='Sampah Menumpuk di Trotoar',
            category='Kebersihan',
            description='Sampah tidak diangkut selama seminggu.',
            location='Jl. Gatot Subroto',
            status='REPORTED',
            reporter=self.warga_b,
        )

    def _get_results(self, response):
        """
        Helper kecil agar test tetap aman jika response menggunakan pagination
        ataupun tidak menggunakan pagination.
        """
        if isinstance(response.data, dict):
            return response.data.get('results', [])
        return response.data

    # ─────────────────────────────────────────────────────────────────────────
    # PRIV-01: Feed Kota Menyembunyikan Identitas Pelapor
    # ─────────────────────────────────────────────────────────────────────────
    def test_PRIV_01_feed_kota_menyembunyikan_identitas_reporter(self):
        """
        [PRIV-01]
        Warga A mengakses feed kota.
        Semua identitas pelapor pada feed publik harus disamarkan.
        """
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get('/api/report/?tab=feed')
        results = self._get_results(response)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(results) > 0, "Feed kota seharusnya memiliki minimal 1 laporan.")

        for laporan in results:
            self.assertEqual(
                laporan['reporter'],
                'Warga Anonim',
                "Reporter pada feed publik harus disamarkan menjadi 'Warga Anonim'."
            )

    # ─────────────────────────────────────────────────────────────────────────
    # PRIV-02: Laporan Saya Menampilkan Nama Asli Pelapor
    # ─────────────────────────────────────────────────────────────────────────
    def test_PRIV_02_laporan_saya_menampilkan_nama_asli(self):
        """
        [PRIV-02]
        Warga A mengakses daftar laporan miliknya sendiri.
        Identitas pelapor harus menampilkan username asli warga A.
        """
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get('/api/report/?tab=my_reports')
        results = self._get_results(response)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(results) > 0, "Harus ada laporan milik Warga A.")

        for laporan in results:
            self.assertEqual(
                laporan['reporter_name'],
                'warga_a',
                "Pada tab my_reports, reporter_name harus menampilkan username asli pemilik laporan."
            )

    # ─────────────────────────────────────────────────────────────────────────
    # PRIV-03: Warga A Tidak Bisa Membaca Draf Milik Warga B
    # ─────────────────────────────────────────────────────────────────────────
    def test_PRIV_03_tidak_bisa_baca_draf_orang_lain(self):
        """
        [PRIV-03]
        Warga A mencoba membaca detail laporan DRAFT milik Warga B.
        Sistem harus menyembunyikan eksistensi draf tersebut dengan HTTP 404.
        """
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get(f'/api/report/{self.draft_milik_b.pk}/')

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Draf milik warga lain harus disembunyikan dengan HTTP 404."
        )

    # ─────────────────────────────────────────────────────────────────────────
    # PRIV-04: Warga A Tidak Bisa Memodifikasi Draf Milik Warga B
    # ─────────────────────────────────────────────────────────────────────────
    def test_PRIV_04_tidak_bisa_modifikasi_draf_orang_lain(self):
        """
        [PRIV-04]
        Warga A mencoba melakukan PUT ke draf milik Warga B.
        Sistem harus menolak dengan HTTP 404 dan data asli tidak boleh berubah.
        """
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        judul_awal = self.draft_milik_b.title
        kategori_awal = self.draft_milik_b.category
        deskripsi_awal = self.draft_milik_b.description
        lokasi_awal = self.draft_milik_b.location
        status_awal = self.draft_milik_b.status

        payload = {
            'title': 'Judul Berhasil Diubah Paksa',
            'category': self.draft_milik_b.category,
            'description': 'Isi draf ini mencoba diubah oleh warga lain.',
            'location': 'Lokasi palsu',
            'status': self.draft_milik_b.status,
        }

        # Act
        response = self.client.put(
            f'/api/report/{self.draft_milik_b.pk}/',
            payload,
            format='json'
        )

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Warga A tidak boleh memodifikasi draf milik Warga B."
        )

        self.draft_milik_b.refresh_from_db()

        self.assertEqual(self.draft_milik_b.title, judul_awal)
        self.assertEqual(self.draft_milik_b.category, kategori_awal)
        self.assertEqual(self.draft_milik_b.description, deskripsi_awal)
        self.assertEqual(self.draft_milik_b.location, lokasi_awal)
        self.assertEqual(self.draft_milik_b.status, status_awal)