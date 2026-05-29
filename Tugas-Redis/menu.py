from produk import (
    tambah_produk, baca_produk,
    update_produk, hapus_produk, daftar_semua_produk
)

def tampilkan_menu():
    print("\n" + "="*40)
    print("   🛒 TOKO ONLINE - MANAJEMEN PRODUK")
    print("="*40)
    print("1. Tambah Produk Baru")
    print("2. Lihat Detail Produk")
    print("3. Update Harga Produk")
    print("4. Update Stok Produk")
    print("5. Hapus Produk")
    print("6. Tampilkan Semua Produk")
    print("0. Keluar")
    print("="*40)

def jalankan():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            id_p = input("ID Produk: ")
            nama = input("Nama Produk: ")
            harga = input("Harga: ")
            stok = input("Stok: ")
            tambah_produk(id_p, nama, harga, stok)

        elif pilihan == "2":
            id_p = input("ID Produk: ")
            baca_produk(id_p)

        elif pilihan == "3":
            id_p = input("ID Produk: ")
            harga_baru = input("Harga baru: ")
            update_produk(id_p, "harga", harga_baru)

        elif pilihan == "4":
            id_p = input("ID Produk: ")
            stok_baru = input("Stok baru: ")
            update_produk(id_p, "stok", stok_baru)

        elif pilihan == "5":
            id_p = input("ID Produk: ")
            hapus_produk(id_p)

        elif pilihan == "6":
            daftar_semua_produk()

        elif pilihan == "0":
            print("👋 Keluar. Sampai jumpa!")
            break

        else:
            print("❌ Pilihan tidak valid.")