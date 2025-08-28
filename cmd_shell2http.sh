#!/usr/bin/env bash

# Archivo de log
LOG_FILE="shell2http.log"

# Puerto
PORT=5050

# Iniciar shell2http con los endpoints definidos
exec shell2http \
    -port "$PORT" \
    -log="$LOG_FILE" \
    -show-errors \
    -include-stderr \
    -add-exit \
    -export-all-vars \
    -form \
    /status 'systemctl --user status sonico.service; systemctl --user status pipewire.service; systemctl status bt_speaker.service' \
    /lista 'ls -hal songs/' \
    /stop 'killall python -9; systemctl --user stop sonico.service' \
    /tag 'source .venv/bin/activate; uv run python add_tag.py' \
    /start 'systemctl --user restart sonico.service' \
    /bt 'sudo systemctl restart bt_speaker.service' \
    /download 'source .venv/bin/activate; uv run python download_song.py $v_yid' \
    GET:/archivo 'echo "<html><body><form method=POST action=/file enctype=multipart/form-data><input type=file name=uplfile><input type=submit></form>"' \
    POST:/file 'cat $filepath_uplfile > songs/$filename_uplfile; echo Ok'
