# Pencarian Jalur

# DATA KOORDINAT SETIAP NODE
koordinat={
    "A": (-6.32631417, 107.0156000),
    "B": (-6.31682806, 107.0084318),
    "C": (-6.30645454, 107.0251967),
    "D": (-6.30985904, 107.0166897),
    "E": (-6.29436752, 107.0220758),
    "F": (-6.32248735, 107.0257286),
    "G": (-6.29591056, 107.0306720)
}

#DATA NAMA SEKOLAH

nama_sekolah= {
    "A":"SDN Cimuning 5",
    "B":"SMPN 10 Kota Bekasi",
    "C":"SMPN 26 Kota Bekasi",
    "D":"SMPN 36 Kota Bekasi",
    "E":"SMPN 40 Kota Bekasi",
    "F":"SMPN 48 Kota Bekasi",
    "G":"SMP Daya Utama"
}

#GRAPH (jarak antar node)
graph = {
    "A":{"B":2.3, "C":4.4,"E":3.5},
    "B":{"A":2.3},
    "C":{"A":4.4,"D":2.0,"E":1.9},
    "D":{"C":2.0,"E":1.9,"F":4.0},
    "E":{"A":3.5,"C":1.9,"D":1.9,"F":4.6,"G":1.6},
    "F":{"D":4.0,"E":4.6,"G":3.7},
    "G":{"E":1.6,"F":3.7}
}
print("Data lokasi dan graph berhasil dimuat.")

# FUNGSI HEURISTIK 

def heuristik(node_awal, node_tujuan):
    x1, y1 = koordinat[node_awal]
    x2, y2 = koordinat[node_tujuan]

    nilai = (x1 - x2) + (y1 - y2)

    return nilai

print("Pengujian Nilai Heuristik")
print("A ke B:", heuristik("A", "B"))
print("A ke C:", heuristik("A", "C"))
print("A ke E:", heuristik("A", "E"))
print("E ke G:", heuristik("E", "G"))