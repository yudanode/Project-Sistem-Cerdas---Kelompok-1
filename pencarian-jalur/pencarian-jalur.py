# Pencarian Jalur
import networkx as nx
import matplotlib.pyplot as plt
import folium
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
    nilai = (x2 - x1) + (y2 - y1)
    return nilai

# FUNGSI A* SEARCH

def astar(start, goal):
    # Inisialisasi daftar OPEN dan CLOSED
    open_list = [start]
    closed_list = []

    # Inisialisasi nilai g dan f
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0

    f_score = {node: float("inf") for node in graph}
    f_score[start] = heuristik(start, goal)

    # Menyimpan node sebelumnya
    came_from = {}

    while open_list:
        # Memilih node dengan nilai f terkecil
        current = min(open_list, key=lambda node: f_score[node])

        # Memeriksa apakah tujuan sudah ditemukan
        if current == goal:
            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()
            return path, g_score[goal]

        open_list.remove(current)
        closed_list.append(current)

        # Memeriksa semua tetangga
        for neighbor, distance in graph[current].items():

            if neighbor in closed_list:
                continue

            # Menghitung jarak aktual
            tentative_g = g_score[current] + distance

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                # Menghitung f(n) = g(n) + h(n)
                f_score[neighbor] = (
                    tentative_g + heuristik(neighbor, goal)
                )

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None, float("inf")


# Visualisasi Graph
def visualisasi_graph(rute):

    G = nx.Graph()

    # Memasukkan hubungan antar-node
    for node, tetangga in graph.items():
        for neighbor, jarak in tetangga.items():
            G.add_edge(node, neighbor, weight=jarak)

    # Posisi node
    posisi = nx.spring_layout(G, seed=42)

    # Membedakan jalur hasil A*
    jalur_edges = list(zip(rute, rute[1:]))

    # Menggambar node
    nx.draw_networkx_nodes(
        G, posisi,
        node_color="lightblue",
        node_size=1500
    )

    # Menggambar seluruh hubungan
    nx.draw_networkx_edges(
        G, posisi,
        edge_color="gray",
        width=1.5
    )

    # Menggambar jalur hasil A*
    nx.draw_networkx_edges(
        G, posisi,
        edgelist=jalur_edges,
        edge_color="red",
        width=3
    )

    # Label node
    nx.draw_networkx_labels(
        G, posisi,
        font_size=12,
        font_weight="bold"
    )

    # Label jarak
    label_jarak = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G, posisi,
        edge_labels=label_jarak,
        font_size=9
    )

    plt.title("Visualisasi Pencarian Rute A*")
    plt.axis("off")
    plt.show()

# VISUALISASI PETA GEOGRAFIS
def visualisasi_peta(rute):

    peta = folium.Map(
    location=koordinat[rute[0]],
    zoom_start=14,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri"
)

    # Menampilkan semua lokasi sekolah
    for kode, lokasi in koordinat.items():

        folium.Marker(
            location=lokasi,
            popup=f"{kode} - {nama_sekolah[kode]}",
            tooltip=nama_sekolah[kode]
        ).add_to(peta)

    # Mengambil koordinat berdasarkan rute A*
    koordinat_rute = [
        koordinat[node] for node in rute
    ]

    # Menggambar jalur hasil A*
    folium.PolyLine(
        locations=koordinat_rute,
        color="red",
        weight=5,
        opacity=0.8,
        tooltip="Rute hasil algoritma A*"
    ).add_to(peta)

    # Menyesuaikan tampilan agar semua sekolah terlihat
    peta.fit_bounds(list(koordinat.values()))

    # Menyimpan peta
    peta.save("peta_rute.html")

    print("\nPeta berhasil disimpan sebagai peta_rute.html")

# PROGRAM UTAMA

def tampilkan_sekolah():
    print("\n=== DAFTAR SEKOLAH ===")
    for kode, nama in nama_sekolah.items():
        print(f"{kode}. {nama}")


def pilih_sekolah(keterangan):
    while True:
        kode = input(
            f"Masukkan kode sekolah {keterangan}: "
        ).upper()

        if kode in nama_sekolah:
            return kode

        print("Kode sekolah tidak ditemukan. Silakan coba lagi.")


print("\n================================")
print(" SISTEM PENCARIAN RUTE SEKOLAH")
print("       ALGORITMA A*")
print("================================")

tampilkan_sekolah()

start = pilih_sekolah("asal")
goal = pilih_sekolah("tujuan")

if start == goal:
    print("\nLokasi asal dan tujuan tidak boleh sama.")

else:
    rute, jarak = astar(start, goal)

    print("\n========== HASIL PENCARIAN ==========")

    if rute:
        print("Lokasi awal  :", nama_sekolah[start])
        print("Lokasi tujuan:", nama_sekolah[goal])

        print("\nUrutan rute perjalanan:")

        for i, node in enumerate(rute, start=1):
            print(f"{i}. {node} - {nama_sekolah[node]}")

        print(f"\nTotal jarak: {jarak:.2f} km")

        # MENAMPILKAN VISUALISASI GRAPH
        visualisasi_graph(rute)

        # Membuat visualisasi peta geografis
        visualisasi_peta(rute)

    else:
        print("Rute tidak ditemukan.")

