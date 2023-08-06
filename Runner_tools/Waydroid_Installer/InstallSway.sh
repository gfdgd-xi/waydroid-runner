#!/bin/bash
# 判断 apt 源里是否有 sway
apt list sway | grep sway
if [[ $? == 0 ]]; then
    echo 从 apt 源安装 Sway
    sudo apt update
    sudo apt install sway aria2 -y
    # 这个包还未构建
    aria2c -x 16 -s 16 http://sway.waydroid-runner.gfdgdxi.top/sway-launcher-icon_1.0.0_all.deb -d /tmp -o sway-desktop-icon.deb
    sudo apt install /tmp/sway-desktop-icon.deb
    exit
fi
if [[ -f /etc/deepin_version ]]; then
    cat /etc/deepin_version | grep 23
    if [[ $? == 0 ]]; then
        # 加 apt 源
        rm -rf /tmp/gfdgd-xi-sources
        mkdir -p /tmp/gfdgd-xi-sources
        wget -P /tmp/gfdgd-xi-sources http://sway.waydroid-runner.gfdgdxi.top/gpg.asc
        wget -P /tmp/gfdgd-xi-sources http://sway.waydroid-runner.gfdgdxi.top/sources/github.list
        gpg --dearmor /tmp/gfdgd-xi-sources/gpg.asc
        #sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FD6EEA1F20CD4B27
        sudo cp -v /tmp/gfdgd-xi-sources/gpg.asc.gpg /etc/apt/trusted.gpg.d/gfdgdxi-list-waydroid-sway.gpg
        sudo cp -v /tmp/gfdgd-xi-sources/github.list /etc/apt/sources.list.d/gfdgdxi-list-waydroid-sway.list
        sudo apt update
        sudo apt install sway -y
        sudo apt install sway-launcher-icon -y
        exit
    fi
fi
echo 该系统暂时无法安装 Sway！