#!/usr/bin/env python3
import re
import sys
import subprocess
import os

def get_youtube_stream_url(url):
    """Obtiene la URL del stream de YouTube usando yt-dlp."""
    try:
        # Usamos yt-dlp para extraer la URL del stream en vivo
        cmd = [
            "yt-dlp",
            "-g",  # Solo obtener la URL
            "--no-playlist",  # No procesar listas de reproducción
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            # La salida puede tener varias líneas (video y audio). Tomamos la primera (video)
            stream_url = result.stdout.strip().split('\n')[0]
            return stream_url
        else:
            print(f"Error con yt-dlp: {result.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Excepción al obtener el stream: {e}", file=sys.stderr)
        return None

def main():
    # Verificar que yt-dlp esté instalado
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp no está instalado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)

    with open('./youtubeLink.txt', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        channel_line = lines[i]
        if i + 1 >= len(lines):
            break

        url_line = lines[i + 1]

        # Verificar que la línea del canal tiene el formato esperado (contiene " - ")
        if ' - ' not in channel_line:
            print(f"Advertencia: línea de canal no válida: '{channel_line}'")
            i += 2
            continue

        # Extraer nombre y grupo
        parts = channel_line.split(' - ', 1)
        if len(parts) < 2:
            print(f"Advertencia: no se pudo parsear la línea: '{channel_line}'")
            i += 2
            continue

        channel_name = parts[0].strip()
        group_title = parts[1].strip().title()

        # Intentar obtener la URL del stream
        if not url_line.startswith('http'):
            print(f"Advertencia: URL no válida: '{url_line}'")
            i += 2
            continue

        stream_url = get_youtube_stream_url(url_line)

        if stream_url:
            # Escribir la entrada M3U
            print(f'#EXTINF:-1 group-title="{group_title}", {channel_name}')
            print(stream_url)
        else:
            print(f"#EXTINF:-1 group-title="{group_title}", {channel_name} (OFFLINE)")
            print(url_line)

        i += 2

if __name__ == "__main__":
    main()
