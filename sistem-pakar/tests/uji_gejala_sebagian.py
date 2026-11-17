
import sys

sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining


DATA_UJI = {
    "P01": ["G01", "G02", "G03"],
    "P02": ["G06", "G07", "G08"],
    "P03": ["G011", "G012", "G013"],
    "P04": ["G016", "G017", "G018"],
    "P05": ["G023", "G025", "G026"],
    "P06": ["G027", "G028", "G029"],
    "P07": ["G031", "G032", "G033"],
}


print("=== PENGUJIAN GEJALA SEBAGIAN ===")

for kode_harapan, gejala in DATA_UJI.items():

    hasil = forward_chaining(gejala)

    kode_hasil = [
        item["kode_penyakit"]
        for item in hasil
    ]

    status = (
        "BERHASIL"
        if kode_harapan in kode_hasil
        else "GAGAL"
    )

    print(
        f"{kode_harapan} | "
        f"Gejala dipilih: {len(gejala)} | "
        f"Kandidat: {', '.join(kode_hasil)} | "
        f"{status}"
    )
