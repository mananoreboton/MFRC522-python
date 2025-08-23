# Sonico

# Install

1. Descargar uv package manager
2. sudo apt install -y python3-dev python3-pip python3-setuptools python3-wheel build-essential
3. sudo apt install ffmpeg
4. wget https://github.com/msoap/shell2http/releases/download/v1.17.0/shell2http_1.17.0_linux_arm64.deb
5. dpkg -i wget shell2http_1.17.0_linux_arm64.deb
4. source .venv/bin/activate
4. uv run python setup.py install
4. sudo nmcli device wifi hotspot ssid SuperSonico password password ifname wlan0

# Use

## Download:
`uv run python download_song.py "https://www.youtube.com/watch?v=WplI0O5n7ag&list=RDWplI0O5n7ag" "Las notas musicales para mi"`





## mfrc522

A python library to read/write RFID tags via the budget MFRC522 RFID module.

This code was published in relation to a [blog post](https://pimylifeup.com/raspberry-pi-rfid-rc522/) and you can find out more about how to hook up your MFRC reader to a Raspberry Pi there.

## Installation

Until the package is on PyPi, clone this repository and run `python setup.py install` in the top level directory.

## Example Code

The following code will read a tag from the MFRC522

```python
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
```
