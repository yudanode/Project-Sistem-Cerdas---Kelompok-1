from django.contrib import admin

from .models import Barang, Permintaan, Persediaan, Produksi, Profile

admin.site.register([Profile, Barang, Permintaan, Persediaan, Produksi])
