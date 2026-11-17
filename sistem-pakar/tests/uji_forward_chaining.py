
import sys

# Menambahkan folder sistem-pakar ke jalur pencarian modul
sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining

# Gejala contoh penyakit Tungro
gejala_dipilih = ["G023", "G025", "G026"]

# Jalankan mesin Forward Chaining
hasil = forward_chaining(gejala_dipilih)

print("=== HASIL FORWARD CHAINING ===")

for item in hasil:
    print(
        f"{item['kode_penyakit']} - {item['nama_penyakit']} "
        f"| Cocok: {item['jumlah_cocok']}/{item['jumlah_syarat']} "
        f"| Kecocokan: {item['persentase_kecocokan']}%"
    )
