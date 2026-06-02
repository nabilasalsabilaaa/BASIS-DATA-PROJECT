from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
    print("Koneksi MongoDB berhasil")

    db = client['hrd_db']
    koleksi = db['karyawan']

    koleksi.delete_many({})

    data = [
        {"nama": "Natasya",   "divisi": "IT",        "gaji": 8500000, "status": "Tetap",   "tahun_masuk": 2019},
        {"nama": "Nabila Salsabila",   "divisi": "Finance",   "gaji": 7200000, "status": "Tetap",   "tahun_masuk": 2018},
        {"nama": "Dewi Astuti MUchtar",     "divisi": "IT",        "gaji": 6800000, "status": "Kontrak", "tahun_masuk": 2021},
        {"nama": "zara", "divisi": "HR",        "gaji": 9000000, "status": "Tetap",   "tahun_masuk": 2017},
        {"nama": "kime",      "divisi": "Finance",   "gaji": 7800000, "status": "Tetap",   "tahun_masuk": 2020},
        {"nama": "indira", "divisi": "IT",        "gaji": 5500000, "status": "Kontrak", "tahun_masuk": 2022},
        {"nama": "jija",      "divisi": "Marketing", "gaji": 6200000, "status": "Tetap",   "tahun_masuk": 2019},
        {"nama": "gatri",  "divisi": "HR",        "gaji": 8200000, "status": "Tetap",   "tahun_masuk": 2016},
        {"nama": "chanyeol",  "divisi": "Marketing", "gaji": 5900000, "status": "Kontrak", "tahun_masuk": 2023},
        {"nama": "baekhyun",    "divisi": "Finance",   "gaji": 7600000, "status": "Tetap",   "tahun_masuk": 2018},
    ]

    koleksi.insert_many(data)
    print("10 data karyawan berhasil dimasukkan!")
    client.close()

except ConnectionFailure as e:
    print(f"Gagal konek ke MongoDB: {e}")
    print("Pastikan MongoDB sudah dijalankan dan mendengarkan pada port 27017")
except Exception as e:
    print(f"Terjadi error: {e}")
    client.close()
