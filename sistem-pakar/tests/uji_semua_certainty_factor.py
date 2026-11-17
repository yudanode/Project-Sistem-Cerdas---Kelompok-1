
import sys
import unittest

sys.path.insert(0, "sistem-pakar")

from engine.certainty_factor import hitung_cf_penyakit
from data.nilai_cf import NILAI_CF


class UjiSemuaCertaintyFactor(unittest.TestCase):

    def test_semua_penyakit(self):
        """Memastikan seluruh tujuh penyakit dapat dihitung."""
        for kode_penyakit, data_gejala in NILAI_CF.items():
            kode_gejala = next(iter(data_gejala))

            hasil = hitung_cf_penyakit(
                kode_penyakit,
                {kode_gejala: 0.8}
            )

            self.assertEqual(hasil["kode_penyakit"], kode_penyakit)
            self.assertGreater(hasil["cf_akhir"], 0)
            self.assertEqual(len(hasil["detail_perhitungan"]), 1)

    def test_gejala_kosong(self):
        """Gejala kosong menghasilkan CF nol."""
        hasil = hitung_cf_penyakit("P05", {})

        self.assertEqual(hasil["cf_akhir"], 0.0)
        self.assertEqual(hasil["persentase"], 0.0)

    def test_gejala_tidak_cocok(self):
        """Gejala valid tetapi bukan milik penyakit menghasilkan CF nol."""
        hasil = hitung_cf_penyakit("P05", {"G034": 1.0})

        self.assertEqual(hasil["cf_akhir"], 0.0)
        self.assertEqual(len(hasil["detail_perhitungan"]), 0)

    def test_bobot_nol(self):
        """Bobot keyakinan nol menghasilkan CF nol."""
        hasil = hitung_cf_penyakit("P05", {"G023": 0.0})

        self.assertEqual(hasil["cf_akhir"], 0.0)

    def test_penyakit_tidak_valid(self):
        """Kode penyakit tidak valid harus menghasilkan ValueError."""
        with self.assertRaises(ValueError):
            hitung_cf_penyakit("P99", {})

    def test_gejala_tidak_valid(self):
        """Kode gejala tidak valid harus menghasilkan ValueError."""
        with self.assertRaises(ValueError):
            hitung_cf_penyakit("P05", {"G999": 1.0})

    def test_bobot_tidak_valid(self):
        """Bobot di luar skala penelitian harus menghasilkan ValueError."""
        with self.assertRaises(ValueError):
            hitung_cf_penyakit("P05", {"G023": 0.7})


if __name__ == "__main__":
    unittest.main(verbosity=2)
