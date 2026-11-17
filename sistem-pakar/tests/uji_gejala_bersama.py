
import sys

sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining


print("=== PENGUJIAN GEJALA BERSAMA ===")

# G014 digunakan oleh aturan P03 dan P06
hasil = forward_chaining(["G014"])

for item in hasil:
    print(
        f"{item['kode_penyakit']} - "
        f"{item['nama_penyakit']} | "
        f"Cocok: {item['jumlah_cocok']}/"
        f"{item['jumlah_syarat']}"
    )

kode_hasil = [
    item["kode_penyakit"]
    for item in hasil
]

if "P03" in kode_hasil and "P06" in kode_hasil:
    print("Pengujian gejala bersama | BERHASIL")
else:
    print("Pengujian gejala bersama | GAGAL")
