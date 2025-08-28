# Sonico

# Install

1. Descargar uv package manager
2. sudo apt install -y python3-dev python3-pip python3-setuptools python3-wheel build-essential
3. sudo apt install ffmpeg
4. uv venv
5. Enable SPI and I2C interfaces with raspi-conf
4. wget https://github.com/msoap/shell2http/releases/download/v1.17.0/shell2http_1.17.0_linux_arm64.deb
4. dpkg -i wget shell2http_1.17.0_linux_arm64.deb
4. source .venv/bin/activate
4. uv run python setup.py install
4. uv run python sonico.py
4. sudo nmcli device wifi hotspot ssid SuperSonico password password ifname wlan0
4. Install PiSugar Power manager (See section)
4. Configure audio (See section)
4. Configure Sonico service (See section)

## Install PiSugar Power manager (See section)
wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
bash pisugar-power-manager.sh -c release
Conection: mrbueno, supersonico, :8421

## Configure audio

1. sudo apt install pipewire libspa-0.2-bluetooth
2. Select Pipewire audio in Advanced options in raspi-config 
3. Restart.

`systemctl --user status pipewire.service`
`systemctl --user status pipewire-pulse.service`

must be active.

4. bluetoothctl

power on
agent on
default-agent
scan on

pair 41:42:70:A4:04:33
trust 41:42:70:A4:04:33
connect 41:42:70:A4:04:33
quit

5. Configure sink (just in case):

`wpctl status`
`wpctl set-default <number_sink>`

6. chmod +x connect_bt.sh
6. sudo cp /home/mrbueno/MFRC522-python/bt_speaker.service /etc/systemd/system/
6. sudo systemctl daemon-reload
6. sudo systemctl enable bt_speaker.service
6. sudo systemctl start bt_speaker.service
6. systemctl status bt_speaker.service

## Configure Sonico

mkdir -p ~/.config/systemd/user
cp /home/mrbueno/MFRC522-python/sonico.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user start sonico.service
systemctl --user status sonico.service
journalctl --user -u sonico.service -f
sudo usermod -aG audio mrbueno

## Configure http endpoints

chmod +x cmd_shell2http.sh 
cp /home/mrbueno/MFRC522-python/shell2http.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable shell2http.service
systemctl --user start shell2http.service
systemctl --user status shell2http.service



# Use



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
