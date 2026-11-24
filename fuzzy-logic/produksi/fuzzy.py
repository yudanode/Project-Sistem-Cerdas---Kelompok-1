"""
Logika Fuzzy Metode Mamdani untuk optimasi produksi barang.

Mengikuti jurnal Nasution & Prakarsa (MIB 4(1), 2020, hal. 131-133):
  - Input  : Permintaan (TURUN, NAIK) dan Persediaan (SEDIKIT, BANYAK)
  - Output : Produksi (BERKURANG, BERTAMBAH)
  - Fungsi keanggotaan: representasi linear
  - Implikasi: MIN, komposisi aturan: MAX, defuzzifikasi: centroid

Rumus fuzzifikasi dan aturan diambil dari kode yang sudah ada; fungsi hanya
diberi parameter batas (min/max) supaya nilainya bisa mengikuti data tiap
tahun dan barang. Nilai bawaan sama dengan contoh jurnal.
"""

# INI BUAT PERMINTAAN
PMT_MIN, PMT_MAX = 2100, 3500
# INI BUAT PERSEDIAAN
PSD_MIN, PSD_MAX = 100, 250
# KAPASITAS
PROD_MIN, PROD_MAX = 1000, 5000


def _klem(v):
    return min(1.0, max(0.0, v))


def permintaan_turun(x, pmt_min=PMT_MIN, pmt_max=PMT_MAX):
    return _klem((pmt_max - x) / (pmt_max - pmt_min))


def permintaan_naik(x, pmt_min=PMT_MIN, pmt_max=PMT_MAX):
    return _klem((x - pmt_min) / (pmt_max - pmt_min))


def persediaan_sedikit(y, psd_min=PSD_MIN, psd_max=PSD_MAX):
    return _klem((psd_max - y) / (psd_max - psd_min))


def persediaan_banyak(y, psd_min=PSD_MIN, psd_max=PSD_MAX):
    return _klem((y - psd_min) / (psd_max - psd_min))


def produksi_berkurang(z, prod_min=PROD_MIN, prod_max=PROD_MAX):
    return (prod_max - z) / (prod_max - prod_min)


def produksi_bertambah(z, prod_min=PROD_MIN, prod_max=PROD_MAX):
    return (z - prod_min) / (prod_max - prod_min)


def evaluasi_aturan(x, y, pmt_min=PMT_MIN, pmt_max=PMT_MAX,
                    psd_min=PSD_MIN, psd_max=PSD_MAX):
    t = permintaan_turun(x, pmt_min, pmt_max)
    n = permintaan_naik(x, pmt_min, pmt_max)
    s = persediaan_sedikit(y, psd_min, psd_max)
    b = persediaan_banyak(y, psd_min, psd_max)
    return {
        "R1 (Turun & Banyak -> Berkurang)": min(t, b),
        "R2 (Turun & Sedikit -> Berkurang)": min(t, s),
        "R3 (Naik & Banyak -> Bertambah)": min(n, b),
        "R4 (Naik & Sedikit -> Bertambah)": min(n, s),
    }


def hitung_produksi(x, y, langkah=1, pmt_min=PMT_MIN, pmt_max=PMT_MAX,
                    psd_min=PSD_MIN, psd_max=PSD_MAX,
                    prod_min=PROD_MIN, prod_max=PROD_MAX):
    if pmt_max <= pmt_min:
        raise ValueError("Permintaan maksimum harus lebih besar dari minimum.")
    if psd_max <= psd_min:
        raise ValueError("Persediaan maksimum harus lebih besar dari minimum.")
    if prod_max <= prod_min:
        raise ValueError("Produksi maksimum harus lebih besar dari minimum.")

    alpha = evaluasi_aturan(x, y, pmt_min, pmt_max, psd_min, psd_max)
    a = list(alpha.values())
    a_berkurang = max(a[0], a[1])
    a_bertambah = max(a[2], a[3])

    # Komponen aturan (jurnal hal. 133): a = prod_min + alpha * (prod_max - prod_min)
    rentang = prod_max - prod_min
    a1 = prod_min + a_berkurang * rentang
    a2 = prod_min + a_bertambah * rentang
    batas_bawah, batas_atas = min(a1, a2), max(a1, a2)

    # Defuzzifikasi centroid; momen (M) dan luas (A) dipisah menjadi 3 daerah
    # [prod_min, batas_bawah], (batas_bawah, batas_atas], (batas_atas, prod_max]
    momen = [0.0, 0.0, 0.0]
    luas = [0.0, 0.0, 0.0]
    z = prod_min
    while z <= prod_max:
        mu = max(
            min(a_berkurang, produksi_berkurang(z, prod_min, prod_max)),
            min(a_bertambah, produksi_bertambah(z, prod_min, prod_max)),
        )
        if z <= batas_bawah:
            i = 0
        elif z <= batas_atas:
            i = 1
        else:
            i = 2
        momen[i] += z * mu
        luas[i] += mu
        z += langkah

    pembilang, penyebut = sum(momen), sum(luas)
    hasil = pembilang / penyebut if penyebut else 0.0
    return {
        "mu_permintaan": {"turun": permintaan_turun(x, pmt_min, pmt_max),
                          "naik": permintaan_naik(x, pmt_min, pmt_max)},
        "mu_persediaan": {"sedikit": persediaan_sedikit(y, psd_min, psd_max),
                          "banyak": persediaan_banyak(y, psd_min, psd_max)},
        "alpha_predikat": alpha,
        "alpha_berkurang": a_berkurang,
        "alpha_bertambah": a_bertambah,
        "a1": a1,
        "a2": a2,
        "momen": momen,
        "luas": luas,
        "produksi": hasil,
    }


if __name__ == "__main__":
    # Contoh dari jurnal: permintaan 3200, persediaan 140
    x, y = 3200, 140
    r = hitung_produksi(x, y)

    print(f"Input: permintaan={x}, persediaan={y}\n")
    print("Derajat keanggotaan:")
    for k, v in {**r["mu_permintaan"], **r["mu_persediaan"]}.items():
        print(f"  {k:<8}: {v:.4f}")
    print("\nAlpha-predikat (MIN):")
    for k, v in r["alpha_predikat"].items():
        print(f"  {k}: {v:.4f}")
    print(f"\nKomposisi MAX -> Berkurang={r['alpha_berkurang']:.4f}, "
          f"Bertambah={r['alpha_bertambah']:.4f}")
    print(f"Hasil defuzzifikasi (centroid): {r['produksi']:.2f} kodi")
