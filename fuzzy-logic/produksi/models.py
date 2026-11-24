from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Level pengguna: administrator, operator order, operator gudang (jurnal hal. 133)."""

    ADMIN = "administrator"
    ORDER = "operator_order"
    GUDANG = "operator_gudang"
    LEVELS = [
        (ADMIN, "Administrator"),
        (ORDER, "Operator Order"),
        (GUDANG, "Operator Gudang"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    level = models.CharField(max_length=20, choices=LEVELS)

    def __str__(self):
        return f"{self.user.username} ({self.get_level_display()})"


class Barang(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nama"]
        verbose_name_plural = "barang"

    def __str__(self):
        return self.nama


class _DataBulanan(models.Model):
    """Dasar untuk data permintaan dan persediaan (ID otomatis PRM000001 / PSD000001)."""

    PREFIX = ""
    kode = models.CharField(max_length=12, unique=True, editable=False)
    tanggal = models.DateField()
    barang = models.ForeignKey(Barang, on_delete=models.PROTECT)
    jumlah = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ["kode"]

    @classmethod
    def kode_berikutnya(cls):
        terakhir = cls.objects.order_by("-kode").values_list("kode", flat=True).first()
        nomor = int(terakhir[len(cls.PREFIX):]) + 1 if terakhir else 1
        return f"{cls.PREFIX}{nomor:06d}"

    def save(self, *args, **kwargs):
        if not self.kode:
            self.kode = self.kode_berikutnya()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode} - {self.barang} - {self.jumlah}"


class Permintaan(_DataBulanan):
    PREFIX = "PRM"


class Persediaan(_DataBulanan):
    PREFIX = "PSD"


class Produksi(models.Model):
    """Hasil prediksi produksi (tabel laporan, jurnal Gambar 8)."""

    kode = models.CharField(max_length=12, unique=True, editable=False)
    barang = models.ForeignKey(Barang, on_delete=models.PROTECT)
    bulan = models.PositiveSmallIntegerField()
    tahun = models.PositiveSmallIntegerField()
    permintaan = models.PositiveIntegerField()
    permintaan_min = models.PositiveIntegerField()
    permintaan_max = models.PositiveIntegerField()
    persediaan = models.PositiveIntegerField()
    persediaan_min = models.PositiveIntegerField()
    persediaan_max = models.PositiveIntegerField()
    hasil = models.FloatField()
    dibuat = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["tahun", "bulan", "kode"]
        constraints = [
            models.UniqueConstraint(fields=["barang", "bulan", "tahun"], name="produksi_unik_periode"),
        ]

    def save(self, *args, **kwargs):
        if not self.kode:
            terakhir = Produksi.objects.order_by("-kode").values_list("kode", flat=True).first()
            nomor = int(terakhir[3:]) + 1 if terakhir else 1
            self.kode = f"PRD{nomor:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode} {self.bulan}/{self.tahun}: {self.hasil:.2f}"
