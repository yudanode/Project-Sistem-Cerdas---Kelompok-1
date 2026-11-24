"""Isi data awal: akun, jenis barang, dan data Tabel 1 jurnal (hal. 131-132)."""
import calendar
from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from produksi.models import Barang, Permintaan, Persediaan, Profile

# (bulan, tahun, permintaan, persediaan) sesuai Tabel 1 jurnal
TABEL_1 = [
    (1, 2019, 2520, 250), (2, 2019, 2100, 174), (3, 2019, 2685, 233),
    (4, 2019, 2740, 154), (5, 2018, 3070, 200), (6, 2018, 2960, 198),
    (7, 2018, 2710, 130), (8, 2017, 3140, 100), (9, 2017, 3120, 131),
    (10, 2017, 2880, 150), (11, 2016, 3500, 115), (12, 2016, 3045, 131),
    (1, 2016, 3200, 140),
]

AKUN = [
    ("admin", "admin123", Profile.ADMIN),
    ("order", "order123", Profile.ORDER),
    ("gudang", "gudang123", Profile.GUDANG),
]


class Command(BaseCommand):
    help = "Membuat akun contoh dan memasukkan data Tabel 1 dari jurnal."

    def handle(self, *args, **options):
        for username, password, level in AKUN:
            user, baru = User.objects.get_or_create(username=username)
            if baru:
                user.set_password(password)
                user.save()
            Profile.objects.get_or_create(user=user, defaults={"level": level})

        barang, _ = Barang.objects.get_or_create(nama="Kaos Belang")

        if Permintaan.objects.exists() or Persediaan.objects.exists():
            self.stdout.write("Data permintaan/persediaan sudah ada, dilewati.")
        else:
            for bulan, tahun, pmt, psd in TABEL_1:
                tgl = date(tahun, bulan, calendar.monthrange(tahun, bulan)[1])
                Permintaan.objects.create(tanggal=tgl, barang=barang, jumlah=pmt)
                Persediaan.objects.create(tanggal=tgl, barang=barang, jumlah=psd)
            self.stdout.write(f"{len(TABEL_1)} baris data Tabel 1 dimasukkan.")

        self.stdout.write(self.style.SUCCESS(
            "Selesai. Akun: admin/admin123, order/order123, gudang/gudang123"))
