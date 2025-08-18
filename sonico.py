from time import sleep
import sys
import sqlite3
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

DB_FILE = "tags.db"

def init_db():
    """Crea la base de datos si no existe"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_tag(tag_id):
    """Busca un tag en la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, count, text FROM tags WHERE id = ?", (tag_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_tag(tag_id, new_count):
    """Actualiza el contador de un tag"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tags SET count = ? WHERE id = ?", (new_count, tag_id))
    conn.commit()
    conn.close()


# Inicializar DB
init_db()

# Inicializar lector
reader = SimpleMFRC522()

try:
    while True:
        print("Acerca un tag al lector...")
        tag_id, text = reader.read()

        # Buscar tag en la base
        row = get_tag(tag_id)

        if row:
            # Si existe en la base, incrementar contador
            id_, count, saved_text = row
            new_count = count + 1
            update_tag(id_, new_count)
            print(f"\n>> TAG ENCONTRADO")
            print(f"ID: {id_}")
            print(f"Texto guardado: {saved_text}")
            print(f"Cantidad de lecturas: {new_count}")
        else:
            # Si no existe, solo mostrar mensaje
            print(f"\n>> TAG NO REGISTRADO")
            print(f"ID: {tag_id}")
            print("No se consiguió en la base de datos.")

        sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)

