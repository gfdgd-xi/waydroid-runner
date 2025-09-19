#!/bin/bash
aria2c -x 16 -s 16 https://github.com/LFRon/libhoudini-11-for-waydroid/releases/download/11.0.1/houdini-install.tar.gz -d /tmp
cd /tmp
tar -xvf houdini-install.tar.gz
cd houdini-install
python3 houdini-install.py
sudo python3 houdini-prop.py
sudo rm /var/lib/waydroid/overlay/system/bin/resetprop #屑山,删掉多放的resetprop防止magisk不识别
rm -rf ../houdini-install
rm ../houdini-install.tar.gz
