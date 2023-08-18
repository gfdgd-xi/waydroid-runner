#!/bin/bash
cd /tmp
rm -rfv widevine-installer
mkdir -p widevine-installer
cd widevine-installer
aria2c -x 16 -s 16 https://jihulab.com/gfdgd-xi/waydroid-image/-/raw/main/Widevine-installer.tar
tar -xvf Widevine-installer.tar
sudo python3 widevine-install.py