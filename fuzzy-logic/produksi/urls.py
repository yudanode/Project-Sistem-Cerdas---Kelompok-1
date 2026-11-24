from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("keluar/", views.logout_view, name="logout"),
    path("beranda/", views.beranda, name="beranda"),
    path("pengguna/", views.kelola_pengguna, name="kelola_pengguna"),
    path("permintaan/", views.data_permintaan, name="data_permintaan"),
    path("persediaan/", views.data_persediaan, name="data_persediaan"),
    path("produksi/", views.data_produksi, name="data_produksi"),
    path("laporan/", views.laporan, name="laporan"),
]
