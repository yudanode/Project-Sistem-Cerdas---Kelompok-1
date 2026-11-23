
import os
import shutil
import traceback
from pathlib import Path

from flask import Flask, render_template, request

# ==========================================
# 1. KONFIGURASI DIREKTORI
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# Membuat folder static jika belum tersedia
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Mengatur direktori kerja
os.chdir(str(BASE_DIR))

print("====================================")
print("LOKASI APP:", Path(__file__).resolve())
print("FOLDER PROYEK:", BASE_DIR)
print("FOLDER STATIC:", STATIC_DIR)
print("====================================")

# ==========================================
# 2. IMPORT ALGORITMA A*
# ==========================================

from road_network import (
    cari_rute_astar,
    tampilkan_peta_rute,
    nama_sekolah
)

# ==========================================
# 3. KONFIGURASI FLASK
# ==========================================

app = Flask(
    __name__,
    static_folder=str(STATIC_DIR),
    template_folder=str(TEMPLATE_DIR)
)

# ==========================================
# 4. DATA SEKOLAH
# ==========================================

data_sekolah = [
    {
        "kode": "A",
        "nama": "SDN Cimuning 5",
        "latitude": -6.32631417,
        "longitude": 107.0156000
    },
    {
        "kode": "B",
        "nama": "SMPN 10 Kota Bekasi",
        "latitude": -6.31682806,
        "longitude": 107.0084318
    },
    {
        "kode": "C",
        "nama": "SMPN 26 Kota Bekasi",
        "latitude": -6.30645454,
        "longitude": 107.0251967
    },
    {
        "kode": "D",
        "nama": "SMPN 36 Kota Bekasi",
        "latitude": -6.30985904,
        "longitude": 107.0166897
    },
    {
        "kode": "E",
        "nama": "SMPN 40 Kota Bekasi",
        "latitude": -6.29436752,
        "longitude": 107.0220758
    },
    {
        "kode": "F",
        "nama": "SMPN 48 Kota Bekasi",
        "latitude": -6.32248735,
        "longitude": 107.0257286
    },
    {
        "kode": "G",
        "nama": "SMP Daya Utama",
        "latitude": -6.29591056,
        "longitude": 107.0306720
    }
]

# ==========================================
# 5. HALAMAN BERANDA
# ==========================================

@app.route("/")
def beranda():

    return render_template("beranda.html")


# ==========================================
# 6. HALAMAN DATA SEKOLAH
# ==========================================

@app.route("/data-sekolah")
def data_sekolah_page():

    return render_template(
        "data_sekolah.html",
        sekolah=data_sekolah
    )


# ==========================================
# 7. HALAMAN PENCARIAN RUTE
# ==========================================

@app.route("/rute-sekolah", methods=["GET", "POST"])
def rute_sekolah():

    hasil = None
    pesan_error = None

    asal = ""
    tujuan = ""

    print("\n====================================")
    print("HALAMAN RUTE DIAKSES")
    print("METHOD:", request.method)
    print("====================================")

    if request.method == "POST":

        asal = request.form.get("asal", "").strip()
        tujuan = request.form.get("tujuan", "").strip()

        print("ASAL:", repr(asal))
        print("TUJUAN:", repr(tujuan))

        if asal not in nama_sekolah or tujuan not in nama_sekolah:

            pesan_error = "Pilihan sekolah tidak valid."

        elif asal == tujuan:

            pesan_error = "Sekolah asal dan tujuan tidak boleh sama."

        else:

            try:

                # ----------------------------------
                # MENCARI RUTE A*
                # ----------------------------------

                print("\nMemulai pencarian rute A*...")

                rute, jarak = cari_rute_astar(
                    asal,
                    tujuan
                )

                print("Rute berhasil ditemukan!")
                print("Jumlah titik:", len(rute))
                print("Jarak:", jarak, "meter")

                # ----------------------------------
                # MEMBUAT PETA
                # ----------------------------------

                print("\nMembuat peta rute...")

                file_asli = tampilkan_peta_rute(
                    rute,
                    asal,
                    tujuan
                )

                file_asli = Path(file_asli).resolve()

                # ----------------------------------
                # MENENTUKAN FILE TUJUAN
                # ----------------------------------

                file_tujuan = (
                    BASE_DIR / "static" / "rute_terakhir.html"
                ).resolve()

                STATIC_DIR.mkdir(
                    parents=True,
                    exist_ok=True
                )

                print("\n=== PEMERIKSAAN FILE PETA ===")
                print("File sumber:", repr(str(file_asli)))
                print("File tujuan:", repr(str(file_tujuan)))
                print("Folder static tersedia:", STATIC_DIR.is_dir())
                print("File sumber tersedia:", file_asli.is_file())

                # ----------------------------------
                # MEMERIKSA FILE SUMBER
                # ----------------------------------

                if not file_asli.is_file():

                    raise FileNotFoundError(
                        f"File sumber peta tidak ditemukan: {file_asli}"
                    )

                # ----------------------------------
                # MENYALIN FILE PETA
                # ----------------------------------

                shutil.copy2(
                    str(file_asli),
                    str(file_tujuan)
                )

                print(
                    "File tujuan berhasil dibuat:",
                    file_tujuan.is_file()
                )

                if not file_tujuan.is_file():

                    raise FileNotFoundError(
                        f"File tujuan tidak ditemukan: {file_tujuan}"
                    )

                # ----------------------------------
                # MENYIAPKAN HASIL
                # ----------------------------------

                hasil = {
                    "asal": nama_sekolah[asal],
                    "tujuan": nama_sekolah[tujuan],
                    "jarak": round(jarak / 1000, 2)
                }

                print("\nPENCARIAN RUTE BERHASIL!")

            except Exception as e:

                print("\n========== DETAIL ERROR ==========")

                traceback.print_exc()

                pesan_error = f"Gagal mencari rute: {e}"

                print("ERROR:", repr(e))
                print("==================================")

    return render_template(
        "rute_sekolah.html",
        sekolah=data_sekolah,
        hasil=hasil,
        pesan_error=pesan_error,
        asal=asal,
        tujuan=tujuan
    )


# ==========================================
# 8. MENJALANKAN FLASK
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
