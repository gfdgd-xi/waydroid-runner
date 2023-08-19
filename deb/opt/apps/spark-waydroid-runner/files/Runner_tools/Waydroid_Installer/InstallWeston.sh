#!/bin/bash
which weston
if [[ $? == 0 ]]; then
    echo Weston have already installed
    exit 0
fi
sudo apt update
sudo apt install weston aria2 -y
rm -rfv /tmp/weston-desktop-icon.deb
aria2c -x 16 -s 16 http://sway.waydroid-runner.gfdgdxi.top/weston-launcher-icon_1.0.0_all.deb -d /tmp -o weston-desktop-icon.deb
sudo apt reinstall /tmp/weston-desktop-icon.deb
