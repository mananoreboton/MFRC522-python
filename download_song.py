#!/usr/bin/env python3
import argparse
import os
import subprocess
import yt_dlp


def download_audio(youtube_id: str, output_dir: str) -> str:
    url = f"https://www.youtube.com/watch?v={youtube_id}"

    # Obtener título seguro
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'audio')[:10]  # primeras 10 letras
        safe_title = "".join(c if c.isalnum() else "_" for c in title)

    # Sin la extensión .mp3 en outtmpl
    final_file = os.path.join(output_dir, safe_title + ".mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, safe_title),  # sin extensión
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return final_file


def cut_audio(input_file: str, start: int, end: int):
    temp_cut = input_file.replace(".mp3", "_cut.mp3")
    command = [
        "ffmpeg", "-y", "-i", input_file,
        "-ss", str(start),
        "-to", str(end),
        "-c:a", "libmp3lame", "-q:a", "2",
        temp_cut
    ]
    subprocess.run(command, check=True)
    os.replace(temp_cut, input_file)


def main():
    parser = argparse.ArgumentParser(description="Descargar canción de YouTube como MP3 (ID) con recorte opcional.")
    parser.add_argument("youtube_id", help="ID del video de YouTube")
    parser.add_argument("--start", type=int, help="Segundo inicial para recorte (opcional)")
    parser.add_argument("--end", type=int, help="Segundo final para recorte (opcional)")
    args = parser.parse_args()

    os.makedirs("songs", exist_ok=True)

    print(f"Descargando video {args.youtube_id}...")
    final_file = download_audio(args.youtube_id, "songs")

    if args.start is not None and args.end is not None:
        print(f"Recortando de {args.start}s a {args.end}s...")
        cut_audio(final_file, args.start, args.end)

    print(f"✅ Canción guardada en: {final_file}")


if __name__ == "__main__":
    main()
