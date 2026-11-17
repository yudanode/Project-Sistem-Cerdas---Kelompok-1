
import sys

sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining

# Pengujian setiap penyakit berdasarkan aturan pada paper
DATA_UJI = {
    "P01": ["G01", "G02", "G03", "G04", "G05"],
    "P02": ["G06", "G07", "G08", "G09", "G010"],
    "P03": ["G011", "G012", "G013", "G014", "G015"],
    "P04": ["G016", "G017", "G018", "G019", "G020"],
    "P05": ["G021", "G022", "G023", "G024", "G025", "G026"],
    "P06": ["G027", "G028", "G029", "G030", "G014"],
    "P07": ["G031", "G032", "G033", "G034"],
}

print("=== PENGUJIAN 7 ATURAN FORWARD CHAINING ===")

for kode_harapan, gejala in DATA_UJI.items():
    hasil = forward_chaining(gejala)

    kode_hasil = [
        item["kode_penyakit"] for item in hasil
    ]

    status = "BERHASIL" if kode_harapan in kode_hasil else "GAGAL"

    print(
        f"{kode_harapan} | "
        f"Kandidat: {', '.join(kode_hasil)} | "
        f"{status}"
    )
