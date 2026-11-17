
import sys

sys.path.insert(0, "sistem-pakar")

from engine.forward_chaining import forward_chaining


print("=== PENGUJIAN VALIDASI GEJALA ===")


# Pengujian 1: Gejala kosong
try:
    hasil = forward_chaining([])

    if hasil == []:
        print("Gejala kosong | BERHASIL")
    else:
        print("Gejala kosong | GAGAL")

except Exception as error:
    print("Gejala kosong | GAGAL:", error)


# Pengujian 2: Kode gejala tidak valid
try:
    forward_chaining(["G999"])

    print("Gejala tidak valid | GAGAL")

except ValueError as error:
    print("Gejala tidak valid | BERHASIL")
    print("Pesan:", error)
