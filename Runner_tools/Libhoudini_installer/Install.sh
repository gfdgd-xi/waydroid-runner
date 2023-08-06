#!/bin/bash
aria2c -x 16 -s 16 https://jihulab.com/gfdgd-xi/waydroid-image/-/raw/main/houdini-install.tar.gz -d /tmp
cd /tmp
tar -xvf houdini-install.tar.gz
cd houdini-install
python3 houdini-install.py
sudo python3 houdini-prop.py
sudo rm /var/lib/waydroid/overlay/system/bin/resetprop #屑山,删掉多放的resetprop防止magisk不识别
rm -rf ../houdini-install
rm ../houdini-install.tar.gz
