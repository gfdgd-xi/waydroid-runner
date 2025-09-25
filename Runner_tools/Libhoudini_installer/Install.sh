#!/bin/bash
aria2c -x 16 -s 16 https://github.com/LFRon/libhoudini-13-for-waydroid/releases/download/13.0.0/houdini-install.tar.gz -d /tmp
cd /tmp
tar -xvf houdini-install.tar.gz
cd houdini-install
python3 houdini-install.py
sudo python3 houdini-prop.py
sudo rm /var/lib/waydroid/overlay/system/bin/resetprop # ,删掉多放的resetprop防止magisk不识别
rm -rf ../houdini-install
rm ../houdini-install.tar.gz
