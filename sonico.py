from time import sleep
import sys
import sqlite3
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import pygame
import os
import logging

DB_FILE = "tags.db"
SONGS_DIR = "songs"   # Carpeta donde se guardan las canciones
LOG_FILE = "sonico.log"

# -------------------- LOGGING --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # opcional: imprime también en consola
    ]
)

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
    """Reproduce un archivo MP3 desde la carpeta songs/"""
    if not args:
        logging.warning("No se indicó nombre de canción.")
        return
    
    song_name = args[0] + ".mp3"
    song_path = os.path.join(SONGS_DIR, song_name)

    if not os.path.exists(song_path):
        logging.error(f"La canción '{song_name}' no se encontró en la carpeta '{SONGS_DIR}'")
        return
    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        logging.info(f"Reproduciendo: {song_name}")
    except Exception as e:
        logging.exception(f"Error al reproducir {song_name}: {e}")


# Diccionario de comandos disponibles
COMMANDS = {
    "play song": cmd_play_song,
    # Se pueden agregar más comandos aquí fácilmente
}


def execute_command(command_text):
    """
    Interpreta el texto guardado en el tag como un comando.
    Formato esperado: "comando arg1 arg2 ..."
    """
    parts = command_text.strip().split()
    if not parts:
        logging.warning("Tag sin comando asociado.")
        return

    for cmd in sorted(COMMANDS.keys(), key=len, reverse=True):
        if command_text.lower().startswith(cmd):
            args = command_text[len(cmd):].strip().split()
            COMMANDS[cmd](args)
            return

    logging.warning(f"Comando no reconocido: {command_text}")



# -------------------- MAIN LOOP --------------------
init_db()
reader = SimpleMFRC522()

def read():
    id, text = reader.read_no_block()
    while not id:
        id, text = reader.read_no_block()
        sleep(0.3)
    return id, text

try:
    while True:
        logging.info("Esperando un tag...")
        tag_id, _ = read()

        row = get_tag(tag_id)

        if row:
            id_, count, saved_text = row
            new_count = count + 1
            update_tag(id_, new_count)

            logging.info(f">> TAG ENCONTRADO | ID: {id_} | Texto: {saved_text} | Lecturas: {new_count}")

            # Ejecutar comando asociado
            execute_command(saved_text)
        else:
            logging.info(f">> TAG NO REGISTRADO | ID: {tag_id}")

        sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
    logging.info("Programa interrumpido con Ctrl+C")
    sys.exit(0)

