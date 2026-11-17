# INI BUAT PERMINTAAN
PMT_MIN, PMT_MAX = 2100, 3500
# INI BUAT PERSEDIAAN
PSD_MIN, PSD_MAX = 100,250
# KAPASITAS
PROD_MIN, PROD_MAX = 1000, 5000


def permintaan_turun(x):
    return min(1.0, max(0.0, (PMT_MAX - x) / (PMT_MAX - PMT_MIN)))

def permintaan_naik(x):
    return min(1.0, max(0.0, (x - PMT_MIN) / (PMT_MAX - PMT_MIN)))

def persediaan_sedikit(y):
    return min(1.0, max(0.0, (PSD_MAX - y) / (PSD_MAX - PSD_MIN)))

def persediaan_banyak(y):
    return min(1.0, max(0.0, (y - PSD_MIN) / (PSD_MAX - PSD_MIN)))

def produksi_berkurang(z):
    return (PROD_MAX - z) / (PROD_MAX - PROD_MIN)

def produksi_bertambah(z):
    return (z - PROD_MIN) / (PROD_MAX - PROD_MIN)


def evaluasi_aturan(x, y):
    t, n = permintaan_turun(x), permintaan_naik(x)
    s, b = persediaan_sedikit(y), persediaan_banyak(y)
    return {
        "R1 (Turun & Banyak -> Berkurang)": min(t, b),
        "R2 (Turun & Sedikit -> Berkurang": min(t, s),
        "R3 (Naik & Banyak -> Bertambah)": min(n, b),
        "R4 (Naik & Sedikit -> Bertambah)": min(n, s),
    }
    
def hitung_produksi(x, y, langkah=1):
    alpha = evaluasi_aturan(x, y)
    a = list(alpha.values())
    a_berkurang = max(a[0], a[1])
    a_bertambah = max(a[2], a[3])
    
    pembilang = penyebut = 0.0
    z = PROD_MIN
    while z <= PROD_MAX:
        mu = max(
            min(a_berkurang, produksi_berkurang(z)),
            min(a_bertambah, produksi_bertambah(z)),
        )
        pembilang += z * mu
        penyebut += mu
        z += langkah
    
    hasil = pembilang / penyebut if penyebut else 0.0
    return {
        "mu_permintaan": {"turun": permintaan_turun(x), "naik": permintaan_naik(x)},
        "mu_persediaan": {"sedikit": persediaan_sedikit(y), "banyak": persediaan_banyak(y)},
        "alpha_predikat": alpha,
        "alpha_berkurang": a_berkurang,
        "alpha_bertambah": a_bertambah,
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