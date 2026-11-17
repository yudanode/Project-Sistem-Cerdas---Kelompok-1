
import sys
import unittest

sys.path.insert(0, "sistem-pakar")

from engine.diagnosis import diagnosis_penyakit
from data.nilai_cf import NILAI_CF
from data.penyakit import PENYAKIT


class UjiSemuaDiagnosis(unittest.TestCase):

    def test_seluruh_penyakit_dapat_didiagnosis(self):
        """Memastikan setiap penyakit dapat muncul sebagai kandidat."""

        for kode_penyakit, data_gejala in NILAI_CF.items():

            with self.subTest(penyakit=kode_penyakit):

                # Gunakan seluruh gejala milik penyakit
                gejala_user = {
                    kode_gejala: 0.8
                    for kode_gejala in data_gejala
                }

                hasil = diagnosis_penyakit(gejala_user)

                kode_kandidat = [
                    item["kode_penyakit"]
                    for item in hasil
                ]

                self.assertIn(kode_penyakit, kode_kandidat)

                # Pastikan nama penyakit sesuai
                hasil_penyakit = next(
                    item for item in hasil
                    if item["kode_penyakit"] == kode_penyakit
                )

                self.assertEqual(
                    hasil_penyakit["nama_penyakit"],
                    PENYAKIT[kode_penyakit]
                )

                self.assertGreater(
                    hasil_penyakit["persentase_keyakinan"],
                    0
                )

    def test_persentase_keyakinan_valid(self):
        """Memastikan persentase CF berada pada rentang 0 sampai 100."""

        gejala_user = {
            "G023": 1.0,
            "G025": 0.8,
            "G026": 0.4,
        }

        hasil = diagnosis_penyakit(gejala_user)

        for item in hasil:
            self.assertGreaterEqual(
                item["persentase_keyakinan"], 0
            )
            self.assertLessEqual(
                item["persentase_keyakinan"], 100
            )

    def test_gejala_tidak_valid(self):
        """Memastikan kode gejala yang tidak terdaftar ditolak."""

        with self.assertRaises(ValueError):
            diagnosis_penyakit({"G999": 1.0})

    def test_semua_hasil_memiliki_detail_cf(self):
        """Memastikan setiap kandidat memiliki detail perhitungan CF."""

        gejala_user = {
            "G023": 1.0,
            "G025": 0.8,
            "G026": 0.4,
        }

        hasil = diagnosis_penyakit(gejala_user)

        for item in hasil:
            self.assertIn("detail_perhitungan_cf", item)
            self.assertIn("cf_akhir", item)
            self.assertIn("persentase_keyakinan", item)


if __name__ == "__main__":
    unittest.main(verbosity=2)
