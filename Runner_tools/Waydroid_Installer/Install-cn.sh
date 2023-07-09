#!/bin/bash
sudo modprobe binder_linux
if [[ $? != 0 ]]; then
    echo 您的内核似乎不支持 binder 模块，是否继续安装？安装完后可能无法使用
    echo 按回车继续
    read
fi
if [[ $XDG_SESSION_TYPE == "x11" ]]; then
    echo 警告：你当前使用的是 x11 协议而非 Wayland 协议，Waydroid 只支持 Wayland 协议
    echo 按回车键忽略该警告继续安装Waydroid本体
    read
fi
echo 请输入版本代号（如focal、bullseye）
read VERSION
curl https://jihulab.com/gfdgd-xi/waydroid-deb/-/raw/main/$VERSION/Packages | grep 404
if [[ $? == 0 ]]; then
    echo 不支持该版本代号
    exit 1
fi
rm -rf /tmp/gfdgd-xi-sources
mkdir -p /tmp/gfdgd-xi-sources
wget -P /tmp/gfdgd-xi-sources http://10.debian.dtk.gfdgdxi.top/gpg.asc
gpg --dearmor /tmp/gfdgd-xi-sources/gpg.asc
sudo cp -v /tmp/gfdgd-xi-sources/gpg.asc.gpg /etc/apt/trusted.gpg.d/gfdgdxi-kernel-list.gpg
sudo bash -c "echo deb http://jihulab.com/gfdgd-xi/waydroid-deb/-/raw/main/$VERSION/ ./ > /etc/apt/sources.list.d/waydroid.list"
sudo apt update
sudo apt install waydroid -y