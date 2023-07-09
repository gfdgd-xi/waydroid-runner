#!/bin/bash
if [[ -f /usr/share/waydroid-extra/images/system.img ]] && [[ -f /usr/share/waydroid-extra/images/vendor.img ]]; then
    echo 已安装镜像，忽略
    exit
fi
sudo modprobe binder_linux
if [[ $? != 0 ]]; then
    echo 您的内核似乎不支持 binder 模块，是否继续安装？安装完后可能无法使用
    echo 按回车继续
    read
fi
cd /tmp
sudo mkdir -p /usr/share/waydroid-extra/images
if [[ -f /usr/share/waydroid-extra/images/system.img ]]; then
    echo 拉取 system.img
    aria2c -x 16 -s 16 https://jihulab.com/gfdgd-xi/waydroid-image/-/raw/main/system.7z
    7z x system.7z
    sudo cp system.img /usr/share/waydroid-extra/images/ -v
fi
if [[ -f /usr/share/waydroid-extra/images/vendor.img ]]; then
    echo 拉取 vendor.img
    aria2c -x 16 -s 16 https://jihulab.com/gfdgd-xi/waydroid-image/-/raw/main/vendor.7z
    7z x vendor.7z
    sudo cp vendor.img /usr/share/waydroid-extra/images/ -v
fi
rm -rf vendor.img vendor.7z system.7z system.img
sudo systemctl restart waydroid-container.service
sudo waydroid init -f