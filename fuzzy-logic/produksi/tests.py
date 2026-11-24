from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from . import fuzzy
from .models import Barang, Permintaan, Persediaan, Produksi, Profile


class FuzzyTest(SimpleTestCase):
    """Contoh jurnal hal. 132: permintaan 3200, persediaan 140."""

    def test_derajat_keanggotaan(self):
        r = fuzzy.hitung_produksi(3200, 140)
        self.assertAlmostEqual(r["mu_permintaan"]["turun"], 300 / 1400)
        self.assertAlmostEqual(r["mu_permintaan"]["naik"], 1100 / 1400)
        self.assertAlmostEqual(r["mu_persediaan"]["sedikit"], 110 / 150)
        self.assertAlmostEqual(r["mu_persediaan"]["banyak"], 40 / 150)

    def test_alpha_predikat(self):
        r = fuzzy.hitung_produksi(3200, 140)
        a = list(r["alpha_predikat"].values())
        self.assertAlmostEqual(a[0], 300 / 1400)   # R1
        self.assertAlmostEqual(a[1], 300 / 1400)   # R2
        self.assertAlmostEqual(a[2], 40 / 150)     # R3
        self.assertAlmostEqual(a[3], 110 / 150)    # R4

    def test_hasil_centroid_dalam_kapasitas(self):
        r = fuzzy.hitung_produksi(3200, 140)
        self.assertTrue(1000 <= r["produksi"] <= 5000)
        # produksi harus bertambah bila permintaan tinggi dan persediaan sedikit
        self.assertGreater(r["produksi"], 3000)

    def test_momen_luas_konsisten(self):
        r = fuzzy.hitung_produksi(3200, 140)
        self.assertAlmostEqual(sum(r["momen"]) / sum(r["luas"]), r["produksi"])

    def test_permintaan_rendah_produksi_berkurang(self):
        rendah = fuzzy.hitung_produksi(2100, 250)["produksi"]
        tinggi = fuzzy.hitung_produksi(3500, 100)["produksi"]
        self.assertLess(rendah, tinggi)

    def test_batas_tidak_valid(self):
        with self.assertRaises(ValueError):
            fuzzy.hitung_produksi(3000, 100, pmt_min=3000, pmt_max=3000)


class AplikasiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_jurnal", verbosity=0)

    def masuk(self, username, password, level):
        return self.client.post(reverse("login"), {
            "username": username, "password": password, "level": level,
        })

    def test_login_level_harus_cocok(self):
        r = self.masuk("admin", "admin123", Profile.ORDER)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Level tidak sesuai")
        r = self.masuk("admin", "admin123", Profile.ADMIN)
        self.assertRedirects(r, reverse("beranda"))

    def test_hak_akses(self):
        self.masuk("order", "order123", Profile.ORDER)
        self.assertEqual(self.client.get(reverse("data_permintaan")).status_code, 200)
        self.assertRedirects(self.client.get(reverse("data_produksi")), reverse("beranda"))

    def test_input_ubah_hapus_permintaan(self):
        self.masuk("order", "order123", Profile.ORDER)
        barang = Barang.objects.first()
        r = self.client.post(reverse("data_permintaan"), {
            "aksi": "input", "tanggal": "2020-01-31", "barang": barang.pk, "jumlah": 1234})
        self.assertEqual(r.status_code, 302)
        obj = Permintaan.objects.get(jumlah=1234)
        self.assertTrue(obj.kode.startswith("PRM"))
        self.client.post(reverse("data_permintaan"), {
            "aksi": "ubah", "pk": obj.pk, "tanggal": "2020-01-31", "barang": barang.pk, "jumlah": 999})
        obj.refresh_from_db()
        self.assertEqual(obj.jumlah, 999)
        self.client.post(reverse("data_permintaan"), {"aksi": "hapus", "pk": obj.pk})
        self.assertFalse(Permintaan.objects.filter(pk=obj.pk).exists())

    def test_alur_produksi_contoh_jurnal(self):
        self.masuk("admin", "admin123", Profile.ADMIN)
        barang = Barang.objects.get(nama="Kaos Belang")
        data = {"tahun_scope": "semua", "barang": barang.pk, "bulan": 1, "tahun": 2016}

        r = self.client.post(reverse("data_produksi"), {**data, "aksi": "pilih"})
        self.assertEqual(r.context["pmt_max"], 3500)
        self.assertEqual(r.context["pmt_min"], 2100)
        self.assertEqual(r.context["psd_max"], 250)
        self.assertEqual(r.context["psd_min"], 100)
        self.assertEqual(r.context["permintaan"], 3200)
        self.assertEqual(r.context["persediaan"], 140)

        r = self.client.post(reverse("data_produksi"), {**data, "aksi": "hitung"})
        self.assertAlmostEqual(r.context["f"]["produksi"], fuzzy.hitung_produksi(3200, 140)["produksi"])

        self.client.post(reverse("data_produksi"), {**data, "aksi": "simpan"})
        p = Produksi.objects.get()
        self.assertEqual((p.bulan, p.tahun, p.permintaan, p.persediaan), (1, 2016, 3200, 140))

        r = self.client.get(reverse("laporan"), {"tahun": 2016})
        self.assertContains(r, p.kode)

    def test_bulan_tanpa_data(self):
        self.masuk("admin", "admin123", Profile.ADMIN)
        barang = Barang.objects.first()
        r = self.client.post(reverse("data_produksi"), {
            "aksi": "hitung", "tahun_scope": "semua", "barang": barang.pk, "bulan": 6, "tahun": 2016})
        self.assertNotIn("f", r.context)
        self.assertContains(r, "belum diinput")
