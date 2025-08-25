#!/bin/bash
# Script para conectar automáticamente al altavoz Bluetooth
# Guarda en ~/miapp/scripts/

DEVICE="41:42:70:A4:04:33"   # <-- reemplaza con la MAC de tu speaker
LOGFILE="$HOME/MFRC522-python/connect_bt.log"

echo "$(date) - Intentando conectar $DEVICE" >> "$LOGFILE"

# Espera un poco a que arranque bluetoothd
sleep 10

# Conexión vía bluetoothctl
echo -e "connect $DEVICE\nquit" | bluetoothctl >> "$LOGFILE" 2>&1

