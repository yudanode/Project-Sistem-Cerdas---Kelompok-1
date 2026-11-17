
import sys

sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining


print("=== PENGUJIAN GEJALA DUPLIKAT ===")

# Pengujian tanpa duplikat
hasil_normal = forward_chaining(
    ["G023", "G025", "G026"]
)

# Pengujian dengan duplikat
hasil_duplikat = forward_chaining(
    ["G023", "G025", "G026", "G023", "G025"]
)

# Ambil hasil penyakit Tungro
tungro_normal = next(
    item for item in hasil_normal
    if item["kode_penyakit"] == "P05"
)

tungro_duplikat = next(
    item for item in hasil_duplikat
    if item["kode_penyakit"] == "P05"
)

print(
    "Jumlah gejala normal:",
    tungro_normal["jumlah_cocok"]
)

print(
    "Jumlah gejala dengan duplikat:",
    tungro_duplikat["jumlah_cocok"]
)

if (
    tungro_normal["jumlah_cocok"]
    == tungro_duplikat["jumlah_cocok"]
):
    print("Pengujian gejala duplikat | BERHASIL")
else:
    print("Pengujian gejala duplikat | GAGAL")
