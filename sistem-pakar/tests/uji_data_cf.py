
import sys

sys.path.insert(0, "sistem-pakar")

from data.nilai_cf import NILAI_CF, BOBOT_KEYAKINAN_USER


print("=== PEMERIKSAAN DATA CERTAINTY FACTOR ===")

print("Jumlah penyakit:", len(NILAI_CF))

for kode_penyakit, data_gejala in NILAI_CF.items():
    print(
        f"{kode_penyakit} | "
        f"Jumlah gejala: {len(data_gejala)}"
    )

print("\n=== PEMERIKSAAN CONTOH TUNGRO ===")

for kode_gejala in ["G023", "G025", "G026"]:
    nilai = NILAI_CF["P05"][kode_gejala]

    print(
        f"{kode_gejala} | "
        f"MB: {nilai['MB']} | "
        f"MD: {nilai['MD']}"
    )

print("\n=== SKALA KEYAKINAN PENGGUNA ===")

for bobot, keterangan in BOBOT_KEYAKINAN_USER.items():
    print(f"{bobot} = {keterangan}")
