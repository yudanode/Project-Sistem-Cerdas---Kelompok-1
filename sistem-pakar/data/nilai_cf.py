
# Data Nilai Certainty Factor
# Sistem Pakar Diagnosis Penyakit Padi
# Sumber: Tabel 4 dan Tabel 5 pada paper penelitian

# Nilai MB (Measure of Belief)
# Nilai MD (Measure of Disbelief)

NILAI_CF = {
    "P01": {
        "G01": {"MB": 0.90, "MD": 0.05},
        "G02": {"MB": 0.80, "MD": 0.10},
        "G03": {"MB": 0.85, "MD": 0.02},
        "G04": {"MB": 0.75, "MD": 0.15},
        "G05": {"MB": 0.60, "MD": 0.25},
    },

    "P02": {
        "G06": {"MB": 0.85, "MD": 0.05},
        "G07": {"MB": 0.80, "MD": 0.10},
        "G08": {"MB": 0.90, "MD": 0.02},
        "G09": {"MB": 0.65, "MD": 0.25},
        "G010": {"MB": 0.70, "MD": 0.20},
    },

    "P03": {
        "G011": {"MB": 0.80, "MD": 0.10},
        "G012": {"MB": 0.85, "MD": 0.05},
        "G013": {"MB": 0.75, "MD": 0.15},
        "G014": {"MB": 0.60, "MD": 0.25},
        "G015": {"MB": 0.60, "MD": 0.30},
    },

    "P04": {
        "G016": {"MB": 0.80, "MD": 0.15},
        "G017": {"MB": 0.85, "MD": 0.05},
        "G018": {"MB": 0.70, "MD": 0.20},
        "G019": {"MB": 0.60, "MD": 0.30},
        "G020": {"MB": 0.75, "MD": 0.15},
    },

    "P05": {
        "G021": {"MB": 0.90, "MD": 0.05},
        "G022": {"MB": 0.90, "MD": 0.10},
        "G023": {"MB": 0.80, "MD": 0.15},
        "G024": {"MB": 0.75, "MD": 0.20},
        "G025": {"MB": 0.85, "MD": 0.10},
        "G026": {"MB": 0.70, "MD": 0.20},
    },

    "P06": {
        "G027": {"MB": 0.85, "MD": 0.10},
        "G028": {"MB": 0.90, "MD": 0.05},
        "G029": {"MB": 0.95, "MD": 0.02},
        "G030": {"MB": 0.80, "MD": 0.15},
        "G014": {"MB": 0.70, "MD": 0.20},
    },

    "P07": {
        "G031": {"MB": 0.90, "MD": 0.10},
        "G032": {"MB": 0.85, "MD": 0.15},
        "G033": {"MB": 0.70, "MD": 0.20},
        "G034": {"MB": 0.65, "MD": 0.25},
    },
}


# Skala tingkat keyakinan pengguna
BOBOT_KEYAKINAN_USER = {
    1.0: "Pasti",
    0.8: "Hampir Pasti",
    0.6: "Kemungkinan Besar",
    0.4: "Mungkin",
    0.2: "Tidak Tahu",
    0.0: "Tidak Ada",
}
