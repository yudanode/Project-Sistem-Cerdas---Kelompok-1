
import sys
import unittest

sys.path.insert(0, "sistem-pakar")

from engine.diagnosis import diagnosis_penyakit


class UjiDiagnosisCampuran(unittest.TestCase):

    def setUp(self):
        self.gejala_campuran = {
            "G01": 0.8,
            "G02": 0.8,
            "G023": 1.0,
            "G025": 0.8,
            "G014": 0.6,
        }

    def test_semua_kandidat_ditemukan(self):
        """Memastikan kandidat dari gejala campuran ditemukan."""

        hasil = diagnosis_penyakit(self.gejala_campuran)

        kode_kandidat = {
            item["kode_penyakit"]
            for item in hasil
        }

        self.assertIn("P01", kode_kandidat)
        self.assertIn("P05", kode_kandidat)
        self.assertIn("P03", kode_kandidat)
        self.assertIn("P06", kode_kandidat)

    def test_semua_kandidat_memiliki_nilai_cf(self):
        """Memastikan seluruh kandidat memiliki hasil CF."""

        hasil = diagnosis_penyakit(self.gejala_campuran)

        for item in hasil:
            self.assertGreaterEqual(item["cf_akhir"], 0)
            self.assertLessEqual(item["cf_akhir"], 1)

    def test_hasil_diurutkan(self):
        """Memastikan hasil diurutkan berdasarkan CF tertinggi."""

        hasil = diagnosis_penyakit(self.gejala_campuran)

        nilai_cf = [
            item["cf_akhir"]
            for item in hasil
        ]

        self.assertEqual(
            nilai_cf,
            sorted(nilai_cf, reverse=True)
        )

    def test_gejala_duplikat_tidak_menggandakan_hasil(self):
        """Memastikan setiap kandidat hanya muncul sekali."""

        hasil = diagnosis_penyakit(self.gejala_campuran)

        kode_kandidat = [
            item["kode_penyakit"]
            for item in hasil
        ]

        self.assertEqual(
            len(kode_kandidat),
            len(set(kode_kandidat))
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
