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

# FUNGSI HEURISTIK HAVERSINE
import math

def heuristik(node_awal, node_tujuan):
    lat1, lon1 = koordinat[node_awal]
    lat2, lon2 = koordinat[node_tujuan]

    # Konversi derajat ke radian
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    #selisih koordinat
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    #rumus haversine
    a=(
        math.sin(dlat/2)**2 
        + math.cos(lat1)
        *math.cos(lat2)
        *math.sin(dlon/2)**2
    )
    c= 2 * math.asin(math.sqrt(a))

    #radius bumi dalam kilometer
    radius_bumi = 6371
    jarak = radius_bumi * c

    # Faktor penyesuaian untuk menjaga
    # heuristik tidak melebihi biaya graph
    return 0.95 * jarak

# Pengujian fungsi heuristik
hasil=heuristik("A", "G")
print("Jarak heuristik A ke G:",
      round(hasil, 3), "km")
