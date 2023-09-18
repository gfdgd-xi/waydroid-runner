#!/bin/bash
which sway
if [[ $? == 0 ]]; then
    echo Sway have already installed
    exit 0
fi
sudo apt update
# 判断 apt 源里是否有 sway
apt list sway | grep sway
if [[ $? == 0 ]]; then
    echo 从 apt 源安装 Sway
    sudo apt update
    sudo apt install sway aria2 -y
    # 这个包还未构建
    rm -rfv /tmp/sway-desktop-icon.deb
    aria2c -x 16 -s 16 http://sway.waydroid-runner.gfdgdxi.top/sway-launcher-icon_1.0.0_all.deb -d /tmp -o sway-desktop-icon.deb
    sudo apt install /tmp/sway-desktop-icon.deb
    exit 0
fi
if [[ -f /etc/deepin_version ]]; then
    cat /etc/deepin_version | grep 23
    if [[ $? == 0 ]]; then
        rm -rf /tmp/gfdgd-xi-sources
        mkdir -p /tmp/gfdgd-xi-sources
        wget -P /tmp/gfdgd-xi-sources http://seafile.jyx2048.com:2345/waydroid-runner/sway-for-deepin23-beta1/gpg.asc
        #wget -P /tmp/gfdgd-xi-sources http://seafile.jyx2048.com:2345/waydroid-runner/sway-for-deepin23-beta1/sources/github.list
        gpg --dearmor /tmp/gfdgd-xi-sources/gpg.asc
        sudo bash -c 'echo "deb http://seafile.jyx2048.com:2345/waydroid-runner/sway-for-deepin23-beta1/ ./" > "/etc/apt/sources.list.d/gfdgdxi-list-lxc.list"'
        sudo apt update
        sudo apt install sway -y
	exit 0
    fi
fi
echo 该系统暂时无法安装 Sway！
exit 1
