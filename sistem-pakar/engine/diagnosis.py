
# Mesin Integrasi Forward Chaining dan Certainty Factor
# Sistem Pakar Diagnosis Penyakit Padi

from engine.forward_chaining import forward_chaining
from engine.certainty_factor import hitung_cf_penyakit
from data.nilai_cf import BOBOT_KEYAKINAN_USER


def diagnosis_penyakit(gejala_user):
    """
    Mengintegrasikan Forward Chaining dan Certainty Factor.

    Parameter:
    - gejala_user: dictionary berisi kode gejala dan bobot
      keyakinan pengguna.

    Contoh:
    {
        "G023": 1.0,
        "G025": 0.8,
        "G026": 0.4
    }

    Proses:
    1. Forward Chaining menentukan kandidat penyakit.
    2. Certainty Factor menghitung keyakinan setiap kandidat.
    3. Hasil diurutkan berdasarkan CF tertinggi.
    """

    # Memastikan input berbentuk dictionary
    if not isinstance(gejala_user, dict):
        raise TypeError("Input gejala_user harus berupa dictionary.")

    # Memastikan bobot keyakinan pengguna valid
    for kode_gejala, bobot in gejala_user.items():
        if bobot not in BOBOT_KEYAKINAN_USER:
            raise ValueError(
                f"Bobot keyakinan tidak valid untuk {kode_gejala}: {bobot}"
            )

    # Tahap 1: Menentukan kandidat penyakit
    kandidat = forward_chaining(list(gejala_user.keys()))

    hasil_diagnosis = []

    # Tahap 2: Menghitung CF setiap kandidat penyakit
    for item in kandidat:

        kode_penyakit = item["kode_penyakit"]

        hasil_cf = hitung_cf_penyakit(
            kode_penyakit,
            gejala_user
        )

        hasil_diagnosis.append({
            "kode_penyakit": kode_penyakit,
            "nama_penyakit": item["nama_penyakit"],
            "gejala_cocok": item["gejala_cocok"],
            "jumlah_cocok": item["jumlah_cocok"],
            "jumlah_syarat": item["jumlah_syarat"],
            "persentase_kecocokan": item["persentase_kecocokan"],
            "detail_perhitungan_cf": hasil_cf["detail_perhitungan"],
            "cf_akhir": hasil_cf["cf_akhir"],
            "persentase_keyakinan": hasil_cf["persentase"],
        })

    # Tahap 3: Mengurutkan hasil berdasarkan CF tertinggi.
    # Jika CF sama, kandidat dengan gejala cocok lebih banyak didahulukan.
    hasil_diagnosis.sort(
        key=lambda item: (
            item["cf_akhir"],
            item["jumlah_cocok"]
        ),
        reverse=True
    )

    return hasil_diagnosis
