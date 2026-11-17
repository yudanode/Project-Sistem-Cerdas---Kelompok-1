
from data.gejala import GEJALA

print("=== DATA GEJALA PENYAKIT PADI ===")
print(f"Jumlah gejala: {len(GEJALA)}")
print()

for kode, nama in GEJALA.items():
    print(f"{kode}: {nama}")
