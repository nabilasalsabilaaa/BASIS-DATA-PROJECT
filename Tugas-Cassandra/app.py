import sys
try:
    import asyncore
except ImportError:
    import pyasyncore
    sys.modules['asyncore'] = pyasyncore
    
import time
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

def cetak_tabel(headers, rows):
    if not rows:
        print(f"{YELLOW}(0 rows){RESET}")
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    border = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    
    print(border)
    header_str = " | ".join([f"{GREEN}{h:<{widths[i]}}{RESET}" for i, h in enumerate(headers)])
    print(f" | {header_str} | ")
    print(border)

    count = 0
    for row in rows:
        row_cells = []
        for i, val in enumerate(row):
            val_str = str(val)
            if "Rp" in val_str or val_str.startswith("ORD-"):
                row_cells.append(f"{YELLOW}{val_str:<{widths[i]}}{RESET}")
            elif val_str.startswith("U0"):
                row_cells.append(f"{MAGENTA}{val_str:<{widths[i]}}{RESET}")
            else:
                row_cells.append(f"{CYAN}{val_str:<{widths[i]}}{RESET}")
        
        print(f" | " + " | ".join(row_cells) + " | ")
        count += 1
        
    print(border)
    print(f"({count} rows)")

def main():
    print("\nMenghubungkan Docker...")
    time.sleep(0.5)
    
    try:
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()
        

        session.set_keyspace('ecommerce_store') 
        print(f"{GREEN}Berhasil terhubung ke Cassandra (Keyspace: ecommerce_store){RESET}")
    except Exception as e:
        print(f"{RED}Gagal terhubung ke Cassandra: {e}{RESET}")
        return

    try:
        session.execute("TRUNCATE orders_by_user;")
        session.execute("TRUNCATE purchases_by_product;")
    except Exception as e:
        print(f"{RED}Gagal mengosongkan tabel: {e}{RESET}")

    transactions = [
        {"user_id": "U001", "order_id": "ORD-101", "order_date": datetime(2026, 6, 1, 10, 0, 0), "product_name": "Laptop Asus", "price": 15000000.0},
        {"user_id": "U002", "order_id": "ORD-102", "order_date": datetime(2026, 6, 2, 11, 30, 0), "product_name": "Laptop Lenovo", "price": 15000000.0},
        {"user_id": "U003", "order_id": "ORD-103", "order_date": datetime(2026, 6, 3, 14, 15, 0), "product_name": "Mouse Wireless", "price": 300000.0},
        {"user_id": "U004", "order_id": "ORD-104", "order_date": datetime(2026, 6, 3, 16, 0, 0), "product_name": "Keyboard Mechanical", "price": 850000.0}
    ]

    print("\nMemasukkan data ke kedua tabel secara bersamaan...")
    insert_user_query = session.prepare("INSERT INTO orders_by_user (user_id, order_date, order_id, product_name, price) VALUES (?, ?, ?, ?, ?)")
    insert_product_query = session.prepare("INSERT INTO purchases_by_product (product_name, order_date, user_id, order_id) VALUES (?, ?, ?, ?)")

    for tx in transactions:
        batch = BatchStatement()
        batch.add(insert_user_query, (tx["user_id"], tx["order_date"], tx["order_id"], tx["product_name"], tx["price"]))
        batch.add(insert_product_query, (tx["product_name"], tx["order_date"], tx["user_id"], tx["order_id"]))
        session.execute(batch)
        print(f"{GREEN} Berhasil memasukkan order {tx['order_id']} ke kedua tabel.{RESET}")
        
    print(f"{GREEN}\nSemua data baru berhasil dimasukkan ke database.{RESET}")
    time.sleep(0.5)

    print(f"\n{BOLD}cqlsh:ecommerce_store> SELECT * FROM orders_by_user;{RESET}")
    all_users = session.execute("SELECT user_id, order_date, order_id, product_name, price FROM orders_by_user")
    headers_user = ['user_id', 'order_date', 'order_id', 'product_name', 'price']
    rows_user = [[r.user_id, r.order_date.strftime('%Y-%m-%d %H:%M:%S'), r.order_id, r.product_name, f"Rp {r.price:,.0f}"] for r in all_users]
    cetak_tabel(headers_user, rows_user)

    print(f"\n{BOLD}cqlsh:ecommerce_store> SELECT * FROM purchases_by_product;{RESET}")
    all_products = session.execute("SELECT product_name, order_date, user_id, order_id FROM purchases_by_product")
    headers_prod = ['product_name', 'order_date', 'user_id', 'order_id']
    rows_prod = [[r.product_name, r.order_date.strftime('%Y-%m-%d %H:%M:%S'), r.user_id, r.order_id] for r in all_products]
    cetak_tabel(headers_prod, rows_prod)
    
    print("\n" + "~"*70)
    input("Data berhasil ditampilkan. Tekan ENTER untuk masuk ke Menu Pencarian...")

    while True:
        print(f"\nMenu pencarian :")
        print("1. Cari Data (Berdasarkan ID atau Nama Produk)")
        print("2. Keluar")
        
        pilihan = input("Pilih opsi (1/2): ").strip()

        if pilihan == "1":
            kata_kunci = input("\nMasukkan ID atau Nama Produk: ").strip()
            
            if kata_kunci.upper().startswith('U') and any(char.isdigit() for char in kata_kunci):
                user_id_clean = kata_kunci.upper()
                print(f"\n{BLUE}Hasil orders dengan ID: '{user_id_clean}' (Tabel: orders_by_user){RESET}")
                
                query = "SELECT user_id, order_date, order_id, product_name, price FROM orders_by_user WHERE user_id = %s"
                rows = session.execute(query, [user_id_clean])
                
                res_rows = [[r.user_id, r.order_date.strftime('%Y-%m-%d %H:%M:%S'), r.order_id, r.product_name, f"Rp {r.price:,.0f}"] for r in rows]
                cetak_tabel(headers_user, res_rows)
            
            else:
                print(f"\n{BLUE}Hasil pembelian produk '{kata_kunci}' (Tabel: purchases_by_product){RESET}")
                
                query = "SELECT product_name, order_date, user_id, order_id FROM purchases_by_product"
                all_rows = session.execute(query)
                
                filtered_rows = []
                for r in all_rows:
                    if kata_kunci.lower() in r.product_name.lower():
                        filtered_rows.append([r.product_name, r.order_date.strftime('%Y-%m-%d %H:%M:%S'), r.user_id, r.order_id])
                
                cetak_tabel(headers_prod, filtered_rows)
            
            input("\nTekan ENTER untuk kembali ke menu...")

        elif pilihan == "2":
            print("\nKeluar dari menu pencarian...")
            break
        else:
            print(f"\n{RED}Opsi tidak valid! Pilih angka 1 atau 2.{RESET}")

    cluster.shutdown()
    print(f"\n{GREEN}Koneksi database ditutup. Program Selesai.{RESET}")

if __name__ == '__main__':
    main()