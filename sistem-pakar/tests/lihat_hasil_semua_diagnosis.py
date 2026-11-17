
import sys

sys.path.insert(0, "sistem-pakar")

from engine.diagnosis import diagnosis_penyakit
from data.nilai_cf import NILAI_CF
from data.penyakit import PENYAKIT


print("=" * 65)
print("SIMULASI HASIL DIAGNOSIS SELURUH PENYAKIT PADI")
print("=" * 65)

for kode_penyakit, data_gejala in NILAI_CF.items():

    # Simulasi pengguna memilih seluruh gejala penyakit
    gejala_user = {
        kode_gejala: 0.8
        for kode_gejala in data_gejala
    }

    hasil = diagnosis_penyakit(gejala_user)

    print("\n" + "=" * 65)
    print(f"SIMULASI: {kode_penyakit} - {PENYAKIT[kode_penyakit]}")
    print("=" * 65)

    print("Gejala yang dipilih:", ", ".join(gejala_user.keys()))

    print("\nDaftar kandidat diagnosis:")

    for nomor, item in enumerate(hasil, start=1):
        print(
            f"{nomor}. {item['kode_penyakit']} - "
            f"{item['nama_penyakit']}"
        )
        print(
            f"   Kecocokan FC : "
            f"{item['jumlah_cocok']}/{item['jumlah_syarat']} "
            f"({item['persentase_kecocokan']}%)"
        )
        print(
            f"   Keyakinan CF : "
            f"{item['persentase_keyakinan']}%"
        )

    if hasil:
        terbaik = hasil[0]
        print("\nHasil peringkat pertama:")
        print(
            f"{terbaik['kode_penyakit']} - "
            f"{terbaik['nama_penyakit']}"
        )
    else:
        print("\nTidak ditemukan kandidat penyakit.")

print("\n" + "=" * 65)
print("SIMULASI SELESAI")
print("=" * 65)
