from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['hrd_db']
koleksi = db['karyawan']

HIJAU = "\033[92m"
BIRU = "\033[94m"
KUNING = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# 1. SEMUA KARYAWAN
print(f"\n{HIJAU}================================================================================{RESET}")
print("DATA ALL KARYAWAN MENTAH:")
print(f"{HIJAU}================================================================================{RESET}")

semua = list(koleksi.find({}, {"_id": 0}))
for k in semua:
    print(f"Nama: {k['nama']}, Divisi: {k['divisi']}, Gaji: {k['gaji']}, Status: {k['status']}, Tahun: {k['tahun_masuk']}")

# 2. QUERY 1: $and + $gt
print(f"\n{BIRU}============================================================{RESET}")
print("HASIL QUERY 1 (TETAP DAN GAJI > 7 JUTA):")
print(f"{BIRU}============================================================{RESET}")

q1 = list(koleksi.find({
    "$and": [
        {"status": "Tetap"},
        {"gaji": {"$gt": 7000000}}
    ]
}, {"_id": 0}))

print(f"Total data ditemukan: {len(q1)}")
for k in q1:
    #<22 bikin nama rata spasi, tanda hubung dan nominal gaji langsung lurus ke bawah
    print(f"-> {k['nama']:<22} - Rp {k['gaji']}")

# 3. QUERY 2: $in
print(f"\n{KUNING}========================================================{RESET}")
print("HASIL QUERY 2 (IT ATAU FINANCE):")
print(f"{KUNING}========================================================{RESET}")

q2 = list(koleksi.find({
    "divisi": {"$in": ["IT", "Finance"]}
}, {"_id": 0}))

print(f"Total data ditemukan: {len(q2)}")
for k in q2:
    #<22 bikin nama rata spasi, tanda hubung dan nama divisi langsung sejajar
    print(f"-> {k['nama']:<22} - {k['divisi']}")

# 4. AGGREGATION PIPELINE
print(f"\n{CYAN}====================================={RESET}")
print("HASIL AGREGASI (RATA-RATA GAJI PER DIVISI):")
print(f"{CYAN}====================================={RESET}")

pipeline = [
    {"$match": {"status": "Tetap"}},
    {"$group": {
        "_id": "$divisi",
        "jumlah": {"$sum": 1},
        "rata_gaji": {"$avg": "$gaji"}
    }},
    {"$sort": {"rata_gaji": -1}}
]
hasil = list(koleksi.aggregate(pipeline))

for h in hasil:
    #<9 bikin nama divisi otomatis rata spasi, jadi garis tengahnya lurus
    print(f"Divisi: {h['_id']:<9} | Total: {h['jumlah']} orang | Rata-rata: Rp {h['rata_gaji']:.2f}")

print(f"{CYAN}==============================================================={RESET}\n")

client.close()