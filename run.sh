#!/bin/bash
echo ""
echo "================================================"
echo "  MAIC-1125 — Detector de Seguridad Industrial"
echo "================================================"
echo ""

# Paso 1: Instalar dependencias de Python
echo "[1/2] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Fallo al instalar dependencias."
    echo "Asegurate de tener Python y pip instalados."
    exit 1
fi

# Paso 2: Arrancar la app Gradio
echo ""
echo "[2/2] Iniciando la app..."
echo "      Abre tu navegador en: http://localhost:7860"
echo "      Presiona Ctrl+C para detener la app."
echo ""
python src/app.py
