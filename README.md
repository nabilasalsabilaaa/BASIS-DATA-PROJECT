# 🛒 Aplikasi Manajemen Produk - Redis Hashes & Sets

Aplikasi CLI (Command Line Interface) sederhana berbasis Python untuk melakukan manajemen katalog produk (CRUD) menggunakan **Redis**. 

Aplikasi ini mendemonstrasikan penggunaan:
* **Redis Hashes** (`HSET`/`HMSET`, `HGETALL`, `DEL`) untuk menyimpan detail objek produk (Nama, Harga, Stok).
* **Redis Sets** (`SADD`, `SREM`, `SMEMBERS`) untuk mengindeks dan menampilkan daftar ID semua produk.

---

## 🚀 Fitur Aplikasi

1. **Tambah Produk Baru** (Menyimpan data ke Hash & ID ke Set)
2. **Lihat Detail Produk** (Mengambil data spesifik berdasarkan ID)
3. **Update Harga Produk** (Mengubah field spesifik pada Hash)
4. **Update Stok Produk** (Mengubah field spesifik pada Hash)
5. **Hapus Produk** (Menghapus Hash & mencabut ID dari Set)
6. **Tampilkan Semua Produk** (Mengambil semua ID dari Set dan menampilkan detailnya)

---

## 🛠️ Prasyarat & Instalasi

Proyek ini dijalankan secara *native* di Windows tanpa menggunakan WSL. Ikuti langkah-langkah berikut untuk setup:

### 1. Instalasi Redis Server (Windows)
1. Unduh installer Redis untuk Windows (.msi) melalui link resmi berikut:  
   👉 [Microsoft Archive Redis Releases](https://github.com/microsoftarchive/redis/releases)
2. Jalankan file `.msi` yang telah diunduh dan ikuti proses instalasi sampai selesai. 
3. *Catatan:* Ingat baik-baik di folder mana kamu menginstal Redis tersebut (misalnya di `C:\Program Files\Redis`).

### 2. Jalankan Redis Server
Sebelum menjalankan aplikasi Python, kamu harus memastikan database Redis sudah aktif:
1. Buka folder tempat instalasi Redis kamu (`C:\Program Files\Redis`).
2. Cari file bernama **`redis-server.exe`**, lalu **klik 2 kali** untuk menjalankannya.
3. Jendela terminal hitam akan muncul menandakan Redis Server telah aktif di port `6379`. *Jangan tutup jendela ini selama aplikasi digunakan.*

### 3. Clone & Setup Project
1. Clone repositori ini ke komputer kamu:
   ```bash
   git clone https://github.com/nabilasalsabilaaa/BASIS-DATA-PROJECT.git
   
2. Masuk ke folder projek:
   ```bash
   cd BASIS-DATA-PROJECT
   cd Tugas-Redis
   
3. Instal library Redis untuk Python via terminal/PowerShell:
   ```bash
   pip install redis
   
---

## 💻 Cara Menjalankan Aplikasi
1. Buka folder proyek ini menggunakan VS Code atau editor pilihanmu.
2. Buka terminal di dalam proyek, lalu jalankan perintah berikut:
    ```powerShell
    py main.py
    atau
    python main.py

3. Jika koneksi berhasil, akan muncul tanda ✅ Terhubung ke Redis! diikuti oleh menu utama aplikasi toko online.

---

## 📂 Struktur File Proyek
- koneksi.py : Mengatur inisialisasi koneksi dan ping testing ke Redis Server lokal.
- produk.py : Berisi fungsi logika bisnis CRUD menggunakan sintaks Redis (hmset, hgetall, hset, delete, sadd, srem, smembers).
- menu.py : Mengatur interface tampilan menu CLI dan menerima input dari user.
- main.py : File utama (entry point) untuk mengeksekusi dan menjalankan aplikasi.
