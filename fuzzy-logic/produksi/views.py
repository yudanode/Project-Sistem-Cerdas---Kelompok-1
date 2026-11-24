from functools import wraps

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from . import fuzzy
from .models import Barang, Permintaan, Persediaan, Produksi, Profile

NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
    "Agustus", "September", "Oktober", "November", "Desember",
]
DAFTAR_BULAN = list(enumerate(NAMA_BULAN, start=1))

JUDUL_BERANDA = {
    Profile.ADMIN: "Halaman Administrator",
    Profile.ORDER: "Halaman Operator Order",
    Profile.GUDANG: "Halaman Operator Gudang",
}


# --------------------------------------------------------------------------- #
# Akses berdasarkan level
# --------------------------------------------------------------------------- #
def level_required(*levels):
    def dekorator(view):
        @wraps(view)
        def bungkus(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            profil = getattr(request.user, "profile", None)
            if profil is None:
                logout(request)
                messages.error(request, "Akun ini belum memiliki level pengguna.")
                return redirect("login")
            if profil.level not in levels:
                messages.error(request, "Anda tidak memiliki akses ke halaman tersebut.")
                return redirect("beranda")
            return view(request, *args, **kwargs)
        return bungkus
    return dekorator


# --------------------------------------------------------------------------- #
# Login / beranda (Gambar 2 dan 3)
# --------------------------------------------------------------------------- #
def login_view(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        return redirect("beranda")

    level_dipilih = request.POST.get("level", "")
    username = request.POST.get("username", "")
    if request.method == "POST":
        password = request.POST.get("password", "")
        if not username or not password or not level_dipilih:
            messages.error(request, "Username, password, dan level harus diisi.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Username atau password salah.")
            elif not hasattr(user, "profile") or user.profile.level != level_dipilih:
                messages.error(request, "Level tidak sesuai dengan akun ini.")
            else:
                login(request, user)
                return redirect("beranda")
    return render(request, "produksi/login.html", {
        "levels": Profile.LEVELS,
        "level_dipilih": level_dipilih,
        "username": username,
    })


def logout_view(request):
    logout(request)
    return redirect("login")


@level_required(Profile.ADMIN, Profile.ORDER, Profile.GUDANG)
def beranda(request):
    level = request.user.profile.level
    return render(request, "produksi/beranda.html", {
        "judul": JUDUL_BERANDA[level],
        "ukuran": "besar",
    })


# --------------------------------------------------------------------------- #
# Kelola pengguna (ubah password; administrator juga mengelola akun)
# --------------------------------------------------------------------------- #
@level_required(Profile.ADMIN, Profile.ORDER, Profile.GUDANG)
def kelola_pengguna(request):
    adalah_admin = request.user.profile.level == Profile.ADMIN
    form_password = PasswordChangeForm(request.user)

    if request.method == "POST":
        aksi = request.POST.get("aksi")
        if aksi == "ubah_password":
            form_password = PasswordChangeForm(request.user, request.POST)
            if form_password.is_valid():
                user = form_password.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password berhasil diubah.")
                return redirect("kelola_pengguna")
            messages.error(request, "Password gagal diubah. Periksa kembali isian Anda.")
        elif aksi == "tambah" and adalah_admin:
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "")
            level = request.POST.get("level", "")
            if not username or not password or level not in dict(Profile.LEVELS):
                messages.error(request, "Username, password, dan level harus diisi.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username sudah dipakai.")
            else:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user, level=level)
                messages.success(request, f"Pengguna {username} ditambahkan.")
            return redirect("kelola_pengguna")
        elif aksi == "hapus" and adalah_admin:
            target = get_object_or_404(User, pk=request.POST.get("pk"))
            if target == request.user:
                messages.error(request, "Anda tidak dapat menghapus akun yang sedang dipakai.")
            else:
                target.delete()
                messages.success(request, "Pengguna dihapus.")
            return redirect("kelola_pengguna")

    return render(request, "produksi/pengguna.html", {
        "judul": "Kelola Pengguna",
        "form_password": form_password,
        "adalah_admin": adalah_admin,
        "pengguna": User.objects.select_related("profile").order_by("username") if adalah_admin else [],
        "levels": Profile.LEVELS,
    })


# --------------------------------------------------------------------------- #
# Data permintaan dan persediaan (Gambar 4 dan 6)
# --------------------------------------------------------------------------- #
def _form_data(model):
    class Form(forms.ModelForm):
        class Meta:
            fields = ["tanggal", "barang", "jumlah"]
            widgets = {"tanggal": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
        Meta.model = model
    return Form


def _kelola_data(request, model, konfigurasi):
    Form = _form_data(model)
    url_name = konfigurasi["url_name"]

    if request.method == "POST":
        aksi = request.POST.get("aksi")
        pk = request.POST.get("pk")
        if aksi == "hapus":
            obj = get_object_or_404(model, pk=pk)
            obj.delete()
            messages.success(request, "Data berhasil dihapus.")
            return redirect(url_name)
        instance = get_object_or_404(model, pk=pk) if aksi == "ubah" else None
        if aksi == "ubah" and instance is None:
            messages.error(request, "Pilih data pada tabel terlebih dahulu.")
            return redirect(url_name)
        form = Form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil " + ("diubah." if aksi == "ubah" else "ditambahkan."))
            return redirect(url_name)
        for galat in form.errors.values():
            messages.error(request, " ".join(galat))
        terpilih = instance
    else:
        terpilih = model.objects.filter(pk=request.GET.get("pilih") or 0).first()
        form = Form(instance=terpilih)

    return render(request, "produksi/data_form.html", {
        **konfigurasi,
        "form": form,
        "terpilih": terpilih,
        "kode_tampil": terpilih.kode if terpilih else model.kode_berikutnya(),
        "daftar": model.objects.select_related("barang").order_by("kode"),
        "barang_list": Barang.objects.all(),
        "ada_barang": Barang.objects.exists(),
    })


@level_required(Profile.ORDER)
def data_permintaan(request):
    return _kelola_data(request, Permintaan, {
        "judul": "Halaman Data Permintaan",
        "url_name": "data_permintaan",
        "label_id": "ID Permintaan",
        "label_jumlah": "Jumlah Permintaan",
        "kolom_kode": "id_permintaan",
    })


@level_required(Profile.GUDANG)
def data_persediaan(request):
    return _kelola_data(request, Persediaan, {
        "judul": "Halaman Data Persediaan",
        "url_name": "data_persediaan",
        "label_id": "ID Persediaan",
        "label_jumlah": "Jumlah Persediaan",
        "kolom_kode": "id_persediaan",
    })


# --------------------------------------------------------------------------- #
# Data produksi (Gambar 7): administrator memproses data -> prediksi produksi
# --------------------------------------------------------------------------- #
def _total_bulanan(model, barang):
    qs = (model.objects.filter(barang=barang)
          .values("tanggal__year", "tanggal__month")
          .annotate(total=Sum("jumlah")))
    return {(r["tanggal__year"], r["tanggal__month"]): r["total"] for r in qs}


def _tahun_tersedia():
    tahun = set()
    for model in (Permintaan, Persediaan):
        tahun.update(d.year for d in model.objects.dates("tanggal", "year"))
    return sorted(tahun)


def _proses_produksi(data, aksi):
    """Hitung semua nilai tampilan untuk halaman Data Produksi.

    Selalu dihitung ulang dari database sehingga isian yang diubah di browser
    tidak memengaruhi hasil.
    """
    ctx = {
        "tahun_scope": data.get("tahun_scope", "semua"),
        "barang_id": data.get("barang", ""),
        "bulan": data.get("bulan", ""),
        "tahun": data.get("tahun", ""),
        "prod_min": settings.PRODUKSI_MIN,
        "prod_max": settings.PRODUKSI_MAX,
    }
    galat = []

    barang = Barang.objects.filter(pk=ctx["barang_id"] or 0).first()
    if barang is None:
        return ctx, ["Pilih jenis barang terlebih dahulu."]

    permintaan_bln = _total_bulanan(Permintaan, barang)
    persediaan_bln = _total_bulanan(Persediaan, barang)

    scope = ctx["tahun_scope"]

    def dalam_scope(d):
        return {k: v for k, v in d.items() if scope == "semua" or k[0] == int(scope)}

    pmt_scope, psd_scope = dalam_scope(permintaan_bln), dalam_scope(persediaan_bln)
    if not pmt_scope or not psd_scope:
        return ctx, ["Data permintaan dan persediaan untuk tahun yang dipilih belum lengkap."]

    ctx.update(
        pmt_max=max(pmt_scope.values()), pmt_min=min(pmt_scope.values()),
        psd_max=max(psd_scope.values()), psd_min=min(psd_scope.values()),
    )

    if ctx["bulan"] and ctx["tahun"]:
        kunci = (int(ctx["tahun"]), int(ctx["bulan"]))
        ctx["permintaan"] = permintaan_bln.get(kunci)
        ctx["persediaan"] = persediaan_bln.get(kunci)
        if ctx["permintaan"] is None or ctx["persediaan"] is None:
            galat.append("Data permintaan atau persediaan pada bulan dan tahun tersebut belum diinput.")
    elif aksi in ("hitung", "simpan"):
        galat.append("Pilih bulan dan tahun yang akan dihitung.")

    if aksi in ("hitung", "simpan") and not galat:
        try:
            ctx["f"] = fuzzy.hitung_produksi(
                ctx["permintaan"], ctx["persediaan"],
                pmt_min=ctx["pmt_min"], pmt_max=ctx["pmt_max"],
                psd_min=ctx["psd_min"], psd_max=ctx["psd_max"],
                prod_min=ctx["prod_min"], prod_max=ctx["prod_max"],
            )
            ctx["f"]["segmen"] = list(zip(ctx["f"]["momen"], ctx["f"]["luas"]))
        except ValueError as e:
            galat.append(str(e))

    ctx["barang_obj"] = barang
    return ctx, galat


@level_required(Profile.ADMIN)
def data_produksi(request):
    ctx = {"tahun_scope": "semua", "barang_id": "", "bulan": "", "tahun": "",
           "prod_min": settings.PRODUKSI_MIN, "prod_max": settings.PRODUKSI_MAX}

    if request.method == "POST":
        aksi = request.POST.get("aksi", "pilih")
        ctx, galat = _proses_produksi(request.POST, aksi)
        for g in galat:
            messages.error(request, g)

        if aksi == "simpan" and not galat and "f" in ctx:
            Produksi.objects.update_or_create(
                barang=ctx["barang_obj"], bulan=int(ctx["bulan"]), tahun=int(ctx["tahun"]),
                defaults=dict(
                    permintaan=ctx["permintaan"], permintaan_min=ctx["pmt_min"], permintaan_max=ctx["pmt_max"],
                    persediaan=ctx["persediaan"], persediaan_min=ctx["psd_min"], persediaan_max=ctx["psd_max"],
                    hasil=ctx["f"]["produksi"],
                ),
            )
            messages.success(request, "Hasil prediksi produksi berhasil disimpan.")
        elif aksi == "pilih" and not galat:
            messages.info(request, "Data berhasil dipilih. Tekan Hitung untuk memperoleh prediksi produksi.")

    ctx.update({
        "judul": "Halaman Data Produksi",
        "barang_list": Barang.objects.all(),
        "tahun_list": _tahun_tersedia(),
        "daftar_bulan": DAFTAR_BULAN,
    })
    return render(request, "produksi/data_produksi.html", ctx)


# --------------------------------------------------------------------------- #
# Laporan (Gambar 8)
# --------------------------------------------------------------------------- #
@level_required(Profile.ADMIN)
def laporan(request):
    tahun_list = sorted(Produksi.objects.values_list("tahun", flat=True).distinct())
    tahun = request.GET.get("tahun", "")
    daftar = Produksi.objects.select_related("barang")
    if tahun:
        try:
            daftar = daftar.filter(tahun=int(tahun))
        except ValueError:
            tahun = ""
    return render(request, "produksi/laporan.html", {
        "judul": "Laporan",
        "tahun_list": tahun_list,
        "tahun": tahun,
        "daftar": daftar,
        "nama_bulan": dict(DAFTAR_BULAN),
    })
