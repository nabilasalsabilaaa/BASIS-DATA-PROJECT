import redis

def get_connection():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    try:
        r.ping()
        print("✅ Terhubung ke Redis!")
    except redis.ConnectionError:
        print("❌ Gagal terhubung ke Redis!")
        exit()
    return r
get_connection()