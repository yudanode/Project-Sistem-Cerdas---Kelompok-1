
import sys
import unittest

sys.path.insert(0, "sistem-pakar")

from engine.diagnosis import diagnosis_penyakit


class UjiDiagnosis(unittest.TestCase):

    def setUp(self):
        self.gejala_tungro = {
            "G023": 1.0,
            "G025": 0.8,
            "G026": 0.4,
        }

    def test_diagnosis_tungro(self):
        """Memastikan Tungro muncul dengan hasil CF yang benar."""
        hasil = diagnosis_penyakit(self.gejala_tungro)

        tungro = next(
            item for item in hasil
            if item["kode_penyakit"] == "P05"
        )

        self.assertEqual(tungro["nama_penyakit"], "Tungro")
        self.assertEqual(tungro["jumlah_cocok"], 3)
        self.assertEqual(tungro["jumlah_syarat"], 6)
        self.assertEqual(tungro["cf_akhir"], 0.888)
        self.assertEqual(tungro["persentase_keyakinan"], 88.8)

    def test_urutan_hasil(self):
        """Memastikan hasil diurutkan dari CF tertinggi."""
        hasil = diagnosis_penyakit(self.gejala_tungro)

        nilai_cf = [
            item["cf_akhir"]
            for item in hasil
        ]

        self.assertEqual(nilai_cf, sorted(nilai_cf, reverse=True))

    def test_gejala_kosong(self):
        """Gejala kosong menghasilkan daftar diagnosis kosong."""
        hasil = diagnosis_penyakit({})

        self.assertEqual(hasil, [])

    def test_input_bukan_dictionary(self):
        """Input selain dictionary harus ditolak."""
        with self.assertRaises(TypeError):
            diagnosis_penyakit(["G023", "G025"])

    def test_bobot_tidak_valid(self):
        """Bobot yang tidak sesuai skala harus ditolak."""
        with self.assertRaises(ValueError):
            diagnosis_penyakit({"G023": 0.7})


if __name__ == "__main__":
    unittest.main(verbosity=2)
