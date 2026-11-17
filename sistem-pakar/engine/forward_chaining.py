
# Mesin Forward Chaining
# Sistem Pakar Diagnosis Penyakit Padi

from data.gejala import GEJALA
from data.penyakit import PENYAKIT
from data.rules import RULES


def forward_chaining(gejala_dipilih):
    """
    Mencocokkan gejala yang dipilih pengguna dengan aturan penyakit.

    Menghasilkan daftar kandidat penyakit berdasarkan jumlah
    gejala yang cocok dengan setiap aturan.
    """

    # Menghilangkan gejala duplikat
    gejala_dipilih = set(gejala_dipilih)

    # Memastikan semua kode gejala valid
    gejala_tidak_valid = gejala_dipilih - set(GEJALA.keys())

    if gejala_tidak_valid:
        raise ValueError(
            f"Kode gejala tidak ditemukan: {gejala_tidak_valid}"
        )

    kandidat_penyakit = []

    # Periksa setiap aturan penyakit
    for kode_penyakit, syarat_gejala in RULES.items():

        # Cari gejala aturan yang dipilih pengguna
        gejala_cocok = [
            kode for kode in syarat_gejala
            if kode in gejala_dipilih
        ]

        # Masukkan penyakit jika minimal ada satu gejala cocok
        if gejala_cocok:
            jumlah_cocok = len(gejala_cocok)
            jumlah_syarat = len(syarat_gejala)

            kandidat_penyakit.append({
                "kode_penyakit": kode_penyakit,
                "nama_penyakit": PENYAKIT[kode_penyakit],
                "gejala_cocok": gejala_cocok,
                "jumlah_cocok": jumlah_cocok,
                "jumlah_syarat": jumlah_syarat,
                "persentase_kecocokan": round(
                    jumlah_cocok / jumlah_syarat * 100, 2
                )
            })

    # Urutkan kandidat dari kecocokan terbanyak
    kandidat_penyakit.sort(
        key=lambda item: item["jumlah_cocok"],
        reverse=True
    )

    return kandidat_penyakit
