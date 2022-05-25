#!/bin/sh
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip

pip3 install logging
pip install pybluez
pip3 install adafruit-circuitpython-neopixel

sudo chmod 777 /etc/rc.local
sudo cat rc_streamPlayer.txt > /etc/rc.local

#enable camera
sudo reboot



