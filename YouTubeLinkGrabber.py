#!/usr/bin/env python3
import subprocess
import sys
import os

def get_stream_url(youtube_url):
    """Obtiene la URL del stream HLS de YouTube usando yt-dlp."""
    try:
        # Comando para extraer solo la URL del stream en vivo
        cmd = [
            "yt-dlp",
            "-g",  # Obtener la URL directa del stream
            "--no-playlist",
            "--format", "best",  # Mejor calidad disponible
            youtube_url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error con yt-dlp: {result.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Excepción al ejecutar yt-dlp: {e}", file=sys.stderr)
        return None

def main():
    # Verificar/Instalar yt-dlp automáticamente
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Instalando yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)

    # Leer el archivo de lista
    try:
        with open('./youtubeLink.txt', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("ERROR: No se encontró el archivo 'youtubeLink.txt'", file=sys.stderr)
        sys.exit(1)

    # Verificar que hay canales
    if not lines:
        print("ERROR: El archivo 'youtubeLink.txt' está vacío", file=sys.stderr)
        sys.exit(1)

    # Procesar la lista (nombre y URL en pares)
    processed_channels = 0
    m3u_output = ["#EXTM3U"]

    for i in range(0, len(lines) - 1, 2):
        if i + 1 >= len(lines):
            break

        name_line = lines[i]
        url_line = lines[i + 1]

        # Verificar formato
        if ' - ' not in name_line:
            print(f"Advertencia: formato incorrecto en '{name_line}'", file=sys.stderr)
            continue

        channel_name, group_title = name_line.split(' - ', 1)
        stream_url = get_stream_url(url_line)

        if stream_url:
            m3u_output.append(f'#EXTINF:-1 group-title="{group_title.title()}", {channel_name}')
            m3u_output.append(stream_url)
            processed_channels += 1
        else:
            print(f"Advertencia: no se pudo obtener el stream para '{channel_name}'", file=sys.stderr)

    # Guardar el archivo M3U generado
    with open('./youtube.m3u', 'w', encoding='utf-8') as f:
        f.write('\n'.join(m3u_output))

    print(f"Lista generada con {processed_channels} canales en 'youtube.m3u'")

if __name__ == "__main__":
    main()
