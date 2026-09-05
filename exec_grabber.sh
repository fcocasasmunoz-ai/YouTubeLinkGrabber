#!/bin/bash
set -e  # Detener el script si ocurre un error

echo "=== Iniciando YouTubeLinkGrabber ==="
echo "Instalando dependencias..."
pip install --user yt-dlp

echo "Ejecutando el script..."
python3 YouTubeLinkGrabber.py

echo "Proceso completado."
