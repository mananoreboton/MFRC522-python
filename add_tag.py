import sqlite3
import sys
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

def add_tag(tag_id, text):
    """Agrega un nuevo tag con count=0"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags (id, count, text) VALUES (?, ?, ?)", (tag_id, 0, text))
    conn.commit()
    conn.close()

def update_tag(tag_id, text):
    """Actualiza el texto de un tag existente (mantiene count)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tags SET text = ? WHERE id = ?", (text, tag_id))
    conn.commit()
    conn.close()


# Verificar que se recibió el texto como argumento
if len(sys.argv) != 2:
    print(f"Uso: python {sys.argv[0]} \"texto_del_tag\"")
    sys.exit(1)

tag_text = sys.argv[1].strip()
if not tag_text:
    print("❌ El texto del tag no puede estar vacío.")
    sys.exit(1)

# Inicializar DB
init_db()

# Inicializar lector
reader = SimpleMFRC522()

try:
    print("Acerca un tag para registrarlo o actualizarlo...")
    tag_id, _ = reader.read()  # ignoramos el texto leído del tag

    row = get_tag(tag_id)

    if row:
        print("\n>> ESTE TAG YA EXISTE")
        print(f"ID: {row[0]}")
        print(f"Texto actual: {row[2]}")
        print(f"Cantidad de lecturas: {row[1]}")

        update_tag(tag_id, tag_text)
        print(f"✅ Tag actualizado con nuevo texto: {tag_text}")
    else:
        add_tag(tag_id, tag_text)
        print("\n>> NUEVO TAG REGISTRADO")
        print(f"ID: {tag_id}")
        print(f"Texto: {tag_text}")
        print("Cantidad de lecturas: 0")

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nProceso interrumpido manualmente.")

finally:
    GPIO.cleanup()
