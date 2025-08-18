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

def add_tag(tag_id, text):
    """Agrega un nuevo tag con count=0"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags (id, count, text) VALUES (?, ?, ?)", (tag_id, 0, text))
    conn.commit()
    conn.close()


# Inicializar DB
init_db()

# Inicializar lector
reader = SimpleMFRC522()

try:
    print("Acerca un tag para registrarlo...")
    tag_id, text = reader.read()

    row = get_tag(tag_id)

    if row:
        print("\n>> ESTE TAG YA EXISTE EN LA BASE")
        print(f"ID: {row[0]}")
        print(f"Texto guardado: {row[2]}")
        print(f"Cantidad de lecturas: {row[1]}")
    else:
        # Si el texto leído está vacío o quieres cambiarlo, pedir por consola
        if not text.strip():
            text = input("El tag no tiene texto. Ingresa un texto para asociar: ")
        else:
            use_text = input(f"Se leyó el texto '{text.strip()}'. ¿Quieres usarlo? (s/n): ")
            if use_text.lower() != 's':
                text = input("Ingresa el nuevo texto: ")

        add_tag(tag_id, text.strip())
        print("\n>> NUEVO TAG REGISTRADO")
        print(f"ID: {tag_id}")
        print(f"Texto: {text.strip()}")
        print("Cantidad de lecturas: 0")

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nProceso interrumpido manualmente.")

finally:
    GPIO.cleanup()

