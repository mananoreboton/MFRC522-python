from time import sleep
import sys
import sqlite3
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pygame

DB_FILE = "tags.db"

# -------------------- BASE DE DATOS --------------------
def init_db():
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
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, count, text FROM tags WHERE id = ?", (tag_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_tag(tag_id, new_count):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tags SET count = ? WHERE id = ?", (new_count, tag_id))
    conn.commit()
    conn.close()


# -------------------- COMANDOS --------------------
def cmd_play_song(args):
    """Reproduce un archivo MP3 usando pygame"""
    if not args:
        print("⚠️  No se indicó nombre de archivo para reproducir.")
        return
    
    song = args[0]
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        print(f"🎵 Reproduciendo: {song}")
    except Exception as e:
        print(f"❌ Error al reproducir {song}: {e}")


# Diccionario de comandos disponibles
COMMANDS = {
    "play song": cmd_play_song,
    # aquí puedes añadir más comandos en el futuro
    # "otro comando": funcion_asociada
}


def execute_command(command_text):
    """
    Interpreta el texto guardado en el tag como un comando.
    Formato esperado: "comando arg1 arg2 ..."
    """
    parts = command_text.strip().split()
    if not parts:
        print("⚠️ Tag sin comando asociado.")
        return

    # el comando puede ser de varias palabras (ej: "play song")
    # probamos del más largo al más corto
    for cmd in sorted(COMMANDS.keys(), key=len, reverse=True):
        if command_text.lower().startswith(cmd):
            args = command_text[len(cmd):].strip().split()
            COMMANDS[cmd](args)
            return

    print(f"⚠️ Comando no reconocido: {command_text}")


# -------------------- MAIN LOOP --------------------
init_db()
reader = SimpleMFRC522()

try:
    while True:
        print("Acerca un tag al lector...")
        tag_id, _ = reader.read()

        row = get_tag(tag_id)

        if row:
            id_, count, saved_text = row
            new_count = count + 1
            update_tag(id_, new_count)

            print(f"\n>> TAG ENCONTRADO")
            print(f"ID: {id_}")
            print(f"Texto guardado: {saved_text}")
            print(f"Cantidad de lecturas: {new_count}")

            # Ejecutar comando asociado
            execute_command(saved_text)
        else:
            print(f"\n>> TAG NO REGISTRADO")
            print(f"ID: {tag_id}")
            print("No se consiguió en la base de datos.")

        sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)

