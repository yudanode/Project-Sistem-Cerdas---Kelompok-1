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


print("\nPengujian Algoritma A*")

rute, jarak = astar("A", "G")

if rute:
    print("Rute yang ditemukan:")

    for node in rute:
        print(f"{node} - {nama_sekolah[node]}")

    print(f"Total jarak: {jarak} km")
else:
    print("Rute tidak ditemukan.")
