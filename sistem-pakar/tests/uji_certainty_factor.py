
import sys

sys.path.insert(0, "sistem-pakar")

from engine.certainty_factor import hitung_cf_penyakit


print("=== PENGUJIAN CERTAINTY FACTOR ===")

# Contoh perhitungan penyakit Tungro dari paper
gejala_user = {
    "G023": 1.0,
    "G025": 0.8,
    "G026": 0.4,
}

hasil = hitung_cf_penyakit("P05", gejala_user)

print("\nPenyakit:", hasil["kode_penyakit"])
print("\nDetail perhitungan:")

for item in hasil["detail_perhitungan"]:
    print(
        f"{item['kode_gejala']} | "
        f"CF Pakar: {item['cf_pakar']} | "
        f"Bobot User: {item['bobot_user']} | "
        f"CF Gejala: {item['cf_gejala']}"
    )

print("\nCF Akhir:", hasil["cf_akhir"])
print("Persentase:", hasil["persentase"], "%")

# Memeriksa kesesuaian dengan contoh paper
if hasil["cf_akhir"] == 0.888:
    print("\nPengujian Certainty Factor | BERHASIL")
else:
    print("\nPengujian Certainty Factor | GAGAL")
