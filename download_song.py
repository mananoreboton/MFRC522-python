#!/usr/bin/env python3
"""
Script para descargar canciones de YouTube como MP3 con recorte opcional.

Requisitos:
    - yt-dlp (pip install yt-dlp)
    - ffmpeg (instalado en el sistema)

Uso:
    python download_song.py <youtube_url> <nombre_salida> [--start SEG_INICIO] [--end SEG_FIN]

Parámetros:
    youtube_url    URL del video de YouTube.
    nombre_salida  Nombre del archivo MP3 de salida (sin extensión).
    --start        (opcional) segundo inicial para recortar (ej: 380 para 6:20).
    --end          (opcional) segundo final para recortar (ej: 461 para 7:41).

Ejemplos:
    Descargar canción completa:
        python download_song.py "https://www.youtube.com/watch?v=abc123" "mi_cancion"

    Descargar solo entre 6:20 y 7:41:
        python download_song.py "https://www.youtube.com/watch?v=abc123" "mi_cancion" --start 380 --end 461
"""

import argparse
import os
import subprocess
import sys

import yt_dlp


def download_audio(url: str, output_path: str) -> str:
    """
    Descarga el audio de YouTube como archivo MP3 completo.
    
    Args:
        url (str): URL del video de YouTube.
        output_path (str): Ruta donde guardar el archivo MP3.
    
    Returns:
        str: Ruta del archivo descargado.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path


def cut_audio(input_file: str, output_file: str, start: int, end: int):
    """
    Recorta un archivo MP3 usando ffmpeg entre dos tiempos dados.
    
    Args:
        input_file (str): Archivo de entrada MP3.
        output_file (str): Archivo de salida MP3.
        start (int): Segundo de inicio.
        end (int): Segundo de fin.
    """
    command = [
        "ffmpeg", "-y", "-i", input_file,
        "-ss", str(start),
        "-to", str(end),
        "-c:a", "libmp3lame", "-q:a", "2",
        output_file
    ]
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description="Descargar canción de YouTube como MP3 con recorte opcional.")
    parser.add_argument("url", help="URL del video de YouTube")
    parser.add_argument("name", help="Nombre del archivo de salida (sin .mp3)")
    parser.add_argument("--start", type=int, help="Segundo inicial para recorte (opcional)")
    parser.add_argument("--end", type=int, help="Segundo final para recorte (opcional)")

    args = parser.parse_args()

    os.makedirs("songs", exist_ok=True)

    temp_file = os.path.join("songs", args.name + "_full.mp3")
    final_file = os.path.join("songs", args.name + ".mp3")

    print(f"Descargando '{args.url}'...")
    download_audio(args.url, temp_file)

    if args.start is not None and args.end is not None:
        print(f"Recortando de {args.start}s a {args.end}s...")
        cut_audio(temp_file, final_file, args.start, args.end)
        os.remove(temp_file)
    else:
        os.rename(temp_file, final_file)

    print(f"✅ Canción guardada en: {final_file}")


if __name__ == "__main__":
    main()

