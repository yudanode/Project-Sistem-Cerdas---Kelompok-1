# Optimasi Produksi Barang — Logika Fuzzy Metode Mamdani (Django)

Aplikasi web berdasarkan jurnal Nasution & Prakarsa, *Jurnal Media Informatika Budidarma* 4(1), 2020, hal. 129–135.
Tampilan meniru form pada Gambar 2–8 jurnal.

## Letak di repo

Salin isi zip ke folder `fuzzy-logic/` di proyek Anda (sejajar dengan `pencarian-jalur/` dan `sistem-pakar/`).
File `fuzzy-logic.py` milik Anda tidak diubah; aplikasi Django memakai salinan logikanya di `produksi/fuzzy.py`.

## Menjalankan

Jalankan semua perintah dari dalam folder `fuzzy-logic/`:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_jurnal      # akun contoh + data Tabel 1 jurnal
python manage.py runserver
```

Buka http://127.0.0.1:8000/

| Level           | Username | Password   | Menu                                                       |
|-----------------|----------|------------|------------------------------------------------------------|
| Administrator   | admin    | admin123   | Kelola Pengguna, Data Produksi, Laporan, Keluar            |
| Operator Order  | order    | order123   | Kelola Pengguna, Data Permintaan, Keluar                   |
| Operator Gudang | gudang   | gudang123  | Kelola Pengguna, Data Persediaan, Keluar                   |

Ganti password setelah login pertama (menu Kelola Pengguna).

## Memeriksa contoh jurnal (permintaan 3200, persediaan 140)

Login sebagai admin → Data Produksi → Tahun: Semua tahun, Jenis Barang: Kaos Belang,
Bulan: Januari, Tahun: 2016 → Pilih → Hitung. Hasil: **3483,33 kodi**.

## Pemetaan ke jurnal

| Jurnal                    | Halaman                       |
|---------------------------|-------------------------------|
| Gambar 2 (LoginForm)      | `/`                           |
| Gambar 3 / 5              | `/beranda/`                   |
| Gambar 4 (Data Permintaan)| `/permintaan/`                |
| Gambar 6 (Data Persediaan)| `/persediaan/`                |
| Gambar 7 (Data Produksi)  | `/produksi/`                  |
| Gambar 8 (Laporan)        | `/laporan/`                   |

Logika fuzzy ada di `produksi/fuzzy.py` dan dapat dijalankan sendiri: `python produksi/fuzzy.py`.

## Catatan

- Permintaan/persediaan per bulan adalah jumlah semua entri pada bulan itu. MAX/MIN diambil dari total bulanan pada tahun yang dipilih (atau semua tahun).
- Produksi MAX/MIN (5000/1000) ada di `config/settings.py` (`PRODUKSI_MAX`, `PRODUKSI_MIN`).
- Nilai M dan A pada Defuzzifikasi adalah jumlah diskret (langkah 1 kodi) pada tiga daerah yang dibatasi a1 dan a2; M total / A total = hasil centroid.
- Jalankan tes: `python manage.py test`.
