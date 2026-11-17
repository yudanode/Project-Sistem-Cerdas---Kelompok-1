
# Mesin Certainty Factor
# Sistem Pakar Diagnosis Penyakit Padi

from data.gejala import GEJALA
from data.nilai_cf import NILAI_CF, BOBOT_KEYAKINAN_USER


def hitung_cf_penyakit(kode_penyakit, gejala_user):
    """
    Menghitung tingkat keyakinan penyakit menggunakan metode
    Certainty Factor.

    Parameter:
    - kode_penyakit: kode penyakit yang akan dihitung.
    - gejala_user: dictionary berisi kode gejala dan bobot
      keyakinan pengguna.

    Contoh:
    {
        "G023": 1.0,
        "G025": 0.8,
        "G026": 0.4
    }
    """

    # Memastikan kode penyakit tersedia
    if kode_penyakit not in NILAI_CF:
        raise ValueError(
            f"Kode penyakit tidak ditemukan: {kode_penyakit}"
        )

    # Memastikan gejala yang dimasukkan valid
    for kode_gejala in gejala_user:
        if kode_gejala not in GEJALA:
            raise ValueError(
                f"Kode gejala tidak ditemukan: {kode_gejala}"
            )

    # Memastikan bobot keyakinan sesuai skala penelitian
    for kode_gejala, bobot_user in gejala_user.items():
        if bobot_user not in BOBOT_KEYAKINAN_USER:
            raise ValueError(
                f"Bobot keyakinan tidak valid untuk {kode_gejala}: "
                f"{bobot_user}"
            )

    data_pakar = NILAI_CF[kode_penyakit]

    detail_perhitungan = []
    cf_gabungan = None

    # Menghitung CF setiap gejala yang sesuai dengan penyakit
    for kode_gejala, nilai_pakar in data_pakar.items():

        if kode_gejala not in gejala_user:
            continue

        mb = nilai_pakar["MB"]
        md = nilai_pakar["MD"]
        bobot_user = gejala_user[kode_gejala]

        # CF pakar = MB - MD
        cf_pakar = mb - md

        # CF gejala = CF pakar x CF pengguna
        cf_gejala = cf_pakar * bobot_user

        detail_perhitungan.append({
            "kode_gejala": kode_gejala,
            "mb": mb,
            "md": md,
            "cf_pakar": round(cf_pakar, 4),
            "bobot_user": bobot_user,
            "cf_gejala": round(cf_gejala, 4),
        })

        # Kombinasi CF secara bertahap
        if cf_gabungan is None:
            cf_gabungan = cf_gejala
        else:
            cf_gabungan = (
                cf_gabungan
                + cf_gejala * (1 - cf_gabungan)
            )

    # Jika tidak ada gejala yang cocok
    if cf_gabungan is None:
        cf_gabungan = 0.0

    return {
        "kode_penyakit": kode_penyakit,
        "detail_perhitungan": detail_perhitungan,
        "cf_akhir": round(cf_gabungan, 4),
        "persentase": round(cf_gabungan * 100, 2),
    }
