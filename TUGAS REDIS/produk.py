from koneksi import get_connection

r = get_connection()

def tambah_produk(id_produk, nama, harga, stok):
    key = f"product:{id_produk}"
    r.hmset(key, mapping={
        "nama": nama,
        "harga": harga,
        "stok": stok
    })
    r.sadd("produk:semua", id_produk) 
    print(f"✅ Produk '{nama}' berhasil ditambahkan dengan key '{key}'")

def baca_produk(id_produk):
    key = f"product:{id_produk}"
    data = r.hgetall(key)
    if data:
        print(f"\n📦 Detail Produk [{key}]")
        print(f"  Nama  : {data['nama']}")
        print(f"  Harga : Rp{data['harga']}")
        print(f"  Stok  : {data['stok']} unit")
    else:
        print(f"❌ Produk dengan ID {id_produk} tidak ditemukan.")

def daftar_semua_produk():
    ids = r.smembers("produk:semua")
    if not ids:
        print("⚠️ Belum ada produk.")
        return
    print("\n📋 Daftar Semua ID Produk:")
    for id_produk in ids:
        data = r.hgetall(f"product:{id_produk}")
        nama = data.get("nama", "?")
        harga = data.get("harga", "?")
        print(f"  - ID: {id_produk} | {nama} | Rp{harga}")
        
        
def update_produk(id_produk, field, nilai_baru):
    key = f"product:{id_produk}"
    if not r.exists(key):
        print(f"❌ Produk ID {id_produk} tidak ditemukan.")
        return
    r.hset(key, field, nilai_baru)
    print(f"✅ Field '{field}' produk ID {id_produk} berhasil diupdate menjadi '{nilai_baru}'")

def hapus_produk(id_produk):
    key = f"product:{id_produk}"
    if not r.exists(key):
        print(f"❌ Produk ID {id_produk} tidak ditemukan.")
        return
    r.delete(key)          
    r.srem("produk:semua", id_produk)  
    print(f"✅ Produk ID {id_produk} berhasil dihapus.")