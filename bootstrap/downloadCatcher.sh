#!/bin/sh
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip

pip3 install opencv-python
pip install picamera
pip install pupil-apriltags
pip3 install logging
pip install pybluez

sudo chmod +xwr /etc/rc.local
sudo cat rc_streamCatcher.txt > /etc/rc.local

#enable camera

