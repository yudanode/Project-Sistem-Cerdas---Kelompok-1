
import os
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

import folium
import osmnx as ox
import networkx as nx


# ==========================================
# 1. KONFIGURASI FOLDER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# 2. DATA KOORDINAT SEKOLAH
# ==========================================

koordinat = {
    "A": (-6.32631417, 107.0156000),
    "B": (-6.31682806, 107.0084318),
    "C": (-6.30645454, 107.0251967),
    "D": (-6.30985904, 107.0166897),
    "E": (-6.29436752, 107.0220758),
    "F": (-6.32248735, 107.0257286),
    "G": (-6.29591056, 107.0306720)
}


nama_sekolah = {
    "A": "SDN Cimuning 5",
    "B": "SMPN 10 Kota Bekasi",
    "C": "SMPN 26 Kota Bekasi",
    "D": "SMPN 36 Kota Bekasi",
    "E": "SMPN 40 Kota Bekasi",
    "F": "SMPN 48 Kota Bekasi",
    "G": "SMP Daya Utama"
}


# ==========================================
# 3. MENGHITUNG TITIK TENGAH WILAYAH
# ==========================================

latitude_tengah = sum(
    lokasi[0] for lokasi in koordinat.values()
) / len(koordinat)

longitude_tengah = sum(
    lokasi[1] for lokasi in koordinat.values()
) / len(koordinat)


# ==========================================
# 4. MENGAMBIL JARINGAN JALAN OPENSTREETMAP
# ==========================================

print("Mengambil jaringan jalan OpenStreetMap...")

G = ox.graph.graph_from_point(
    (latitude_tengah, longitude_tengah),
    dist=5000,
    network_type="drive"
)

print("Jaringan jalan berhasil diambil!")
print("Jumlah titik jalan:", len(G.nodes))
print("Jumlah ruas jalan:", len(G.edges))


# ==========================================
# 5. MENGHUBUNGKAN SEKOLAH KE JARINGAN JALAN
# ==========================================

print("\nMenghubungkan sekolah ke jaringan jalan...")

sekolah_nodes = {}

for kode, lokasi in koordinat.items():

    latitude, longitude = lokasi

    node_jalan = ox.distance.nearest_nodes(
        G,
        X=longitude,
        Y=latitude
    )

    sekolah_nodes[kode] = node_jalan

    print(
        kode,
        "-",
        nama_sekolah[kode],
        "-> Node jalan:",
        node_jalan
    )

print("\nSemua sekolah berhasil dihubungkan!")


# ==========================================
# 6. GRAPH UNTUK ALGORITMA A*
# ==========================================

G_astar = G


# ==========================================
# 7. FUNGSI HEURISTIK HAVERSINE
# ==========================================

def heuristik(node1, node2):

    lat1 = radians(G_astar.nodes[node1]["y"])
    lon1 = radians(G_astar.nodes[node1]["x"])

    lat2 = radians(G_astar.nodes[node2]["y"])
    lon2 = radians(G_astar.nodes[node2]["x"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return 6371000 * c


# ==========================================
# 8. FUNGSI PENCARIAN RUTE A*
# ==========================================

def cari_rute_astar(kode_awal, kode_tujuan):

    if kode_awal not in sekolah_nodes:
        raise ValueError("Kode sekolah asal tidak ditemukan.")

    if kode_tujuan not in sekolah_nodes:
        raise ValueError("Kode sekolah tujuan tidak ditemukan.")

    node_awal = sekolah_nodes[kode_awal]
    node_tujuan = sekolah_nodes[kode_tujuan]

    rute = nx.astar_path(
        G_astar,
        source=node_awal,
        target=node_tujuan,
        heuristic=heuristik,
        weight="length"
    )

    jarak = sum(
        min(
            data["length"]
            for data in G_astar[u][v].values()
        )
        for u, v in zip(rute[:-1], rute[1:])
    )

    return rute, jarak


# ==========================================
# 9. FUNGSI MEMBUAT PETA RUTE
# ==========================================

def tampilkan_peta_rute(rute, kode_awal, kode_tujuan):

    # Mengambil geometri ruas jalan dari rute A*
    edges = ox.routing.route_to_gdf(
        G_astar,
        rute,
        weight="length"
    )

    koordinat_jalan = []

    # Menggabungkan koordinat setiap ruas jalan
    for geometry in edges.geometry:

        if geometry is None:
            continue

        if geometry.geom_type == "LineString":

            koordinat_jalan.extend(
                [
                    (lat, lon)
                    for lon, lat in geometry.coords
                ]
            )

        elif geometry.geom_type == "MultiLineString":

            for line in geometry.geoms:

                koordinat_jalan.extend(
                    [
                        (lat, lon)
                        for lon, lat in line.coords
                    ]
                )

    if not koordinat_jalan:
        raise ValueError("Geometri jalan untuk rute tidak ditemukan.")

    # Membuat peta
    peta = folium.Map(
        location=koordinat[kode_awal],
        zoom_start=15,
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/"
            "rest/services/World_Street_Map/MapServer/"
            "tile/{z}/{y}/{x}"
        ),
        attr="Tiles © Esri"
    )

    # Menampilkan semua sekolah
    for kode, lokasi in koordinat.items():

        folium.Marker(
            location=lokasi,
            popup=f"{kode} - {nama_sekolah[kode]}",
            tooltip=nama_sekolah[kode]
        ).add_to(peta)

    # Menampilkan titik awal
    folium.Marker(
        location=koordinat[kode_awal],
        popup=f"Titik Awal: {nama_sekolah[kode_awal]}",
        icon=folium.Icon(color="green")
    ).add_to(peta)

    # Menampilkan titik tujuan
    folium.Marker(
        location=koordinat[kode_tujuan],
        popup=f"Titik Tujuan: {nama_sekolah[kode_tujuan]}",
        icon=folium.Icon(color="red")
    ).add_to(peta)

    # Menampilkan jalur hasil A*
    folium.PolyLine(
        locations=koordinat_jalan,
        color="red",
        weight=6,
        opacity=0.85,
        tooltip="Rute A* melalui jaringan jalan"
    ).add_to(peta)

    # Menyesuaikan tampilan peta dengan rute
    peta.fit_bounds(koordinat_jalan)

    # Menyimpan peta di folder proyek
    nama_file = (
        BASE_DIR / f"rute_{kode_awal}_ke_{kode_tujuan}.html"
    )

    peta.save(str(nama_file))

    print("\nPeta berhasil disimpan:", nama_file)
    print("File ditemukan:", nama_file.exists())

    return nama_file


# ==========================================
# 10. PENGUJIAN A* JIKA FILE DIJALANKAN LANGSUNG
# ==========================================

if __name__ == "__main__":

    print("\nPENGUJIAN A* JARINGAN JALAN")

    rute, jarak = cari_rute_astar("A", "G")

    print("Asal:", nama_sekolah["A"])
    print("Tujuan:", nama_sekolah["G"])

    print(
        "Jumlah titik yang dilewati:",
        len(rute)
    )

    print(
        "Total jarak:",
        round(jarak / 1000, 2),
        "km"
    )

    tampilkan_peta_rute(
        rute,
        "A",
        "G"
    )
