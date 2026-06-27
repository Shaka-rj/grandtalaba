import sqlite3
import os
import requests

DB_NAME = "grandtalaba.db"

os.makedirs("icons", exist_ok=True)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("SELECT slug, iconurl, name FROM universities")
rows = cursor.fetchall()

for slug, iconurl, name in rows:

    if not iconurl or not slug:
        continue

    try:
        r = requests.get(iconurl, timeout=30)
        r.raise_for_status()

        file_path = f"icons/{slug}.png"

        with open(file_path, "wb") as f:
            f.write(r.content)

        print("Yuklandi:", slug)

    except Exception as e:
        print("Xato:", name, e)

conn.close()

print("Barcha iconlar yuklab olindi.")