# Sonico

# previously 

1. user must be mrbueno
1. enable wifi and configure it via raspi-conf
1. sudo apt install openssh-server

# Install

1. sudo apt install -y python3-dev python3-pip python3-setuptools python3-wheel build-essential ffmpeg pipewire libspa-0.2-bluetooth expect mpg123 python3-full git tree vim libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libfreetype6-dev libjpeg-dev libpng-dev

1. Enable SPI and I2C interfaces with raspi-conf
1. Select Pipewire audio in Advanced options in raspi-config 
1. enable console auto-login in raspi-conf (configure boot to console if needed: systems Options -> S5 and S6)
1. Restart
1. sudo usermod -aG audio mrbueno
1. mkdir -p ~/.config/systemd/user
1. Configure audio services (See section)
1. Configure python scripts (4B)
1. Configure Sonico service (See section)
 

## Configure audio services

`systemctl --user status pipewire.service`
`systemctl --user status pipewire-pulse.service`

must be active.

6. bluetoothctl

power on
agent on
default-agent
scan on

pair 41:42:70:A4:04:33
trust 41:42:70:A4:04:33
connect 41:42:70:A4:04:33
quit

6. Configure sink (just in case):

`wpctl status`
`wpctl set-default <number_sink>`

6. chmod +x connect_bt.sh
6. sudo cp /home/mrbueno/MFRC522-python/bt_speaker.service /etc/systemd/system/
6. sudo systemctl daemon-reload
6. sudo systemctl enable bt_speaker.service
6. sudo systemctl start bt_speaker.service
6. systemctl status bt_speaker.service
6. sudo usermod -aG audio,rtkit $USER
6. sudo shutdown -r now
6. groups
6. ps -o pid,comm,ni,rtprio -p $(pidof pipewire)
6. mkdir -p ~/.config/pipewire/pipewire.conf.d
6. cp 99-realtime.conf ~/.config/pipewire/pipewire.conf.d/
6. systemctl --user restart pipewire
6. systemctl --user restart wireplumber
6. ps -o pid,comm,ni,rtprio -p $(pidof pipewire)

## Configure python scripts (4B)

1. chmod +x sonico.py
1. download uv: curl -LsSf https://astral.sh/uv/install.sh | sh
4. uv venv
4. source .venv/bin/activate
4. uv run python setup.py install
4. uv run python sonico.py

### Configure python scripts, alternative way (NOT TESTED)

1. chmod +x sonico.py
1. apt install python3-pygame python3-pygame-sdl2 python3-sdl2
1. curl -LsSf https://astral.sh/uv/install.sh | sh
1. uv venv
1. source .venv/bin/activate
1. python -m ensurepip --upgrade
1. python -m pip install RPi.GPIO
1. python -m pip install spidev
1. python -m pip install pygame


## Configure Sonico

cp /home/mrbueno/MFRC522-python/sonico.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable sonico.service
systemctl --user start sonico.service
systemctl --user status sonico.service
journalctl --user -u sonico.service -f

## Optional

4. Configure http endpoints
4. Install PiSugar Power manager (See section)
4. sudo nmcli device wifi hotspot ssid SuperSonico password password ifname wlan0
4. COnfigure Pipewire as real time: sudo chrt -r -p 20 $(pidof pipewire)

## Install PiSugar Power manager (See section)

wget https://cdn.pisugar.com/release/pisugar-power-manager.sh
bash pisugar-power-manager.sh -c release
Conection: mrbueno, supersonico, :8421

## Configure http endpoints

wget https://github.com/msoap/shell2http/releases/download/v1.17.0/shell2http_1.17.0_linux_arm64.deb
dpkg -i wget shell2http_1.17.0_linux_arm64.deb
chmod +x cmd_shell2http.sh 
cp /home/mrbueno/MFRC522-python/shell2http.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable shell2http.service
systemctl --user start shell2http.service
systemctl --user status shell2http.service


## Troubleshotting

sudo usermod -aG video mrbueno   # para vcgencmd
sudo usermod -aG spi mrbueno     # para MFRC522 (SPI)
sudo usermod -aG gpio mrbueno    # para acceso GPIO
sudo usermod -aG adm mrbueno


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
