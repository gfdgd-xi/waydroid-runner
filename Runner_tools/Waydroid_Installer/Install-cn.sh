#!/bin/bash
sudo modprobe binder_linux
lsmod | grep -e binder_linux
if [[ $? != 0 ]] && [[ -f /dev/binder ]] && [[ -f /dev/binderfs ]]; then
    echo 您的内核似乎不支持 binder 模块，是否继续安装？安装完后可能无法使用
    echo 按回车继续
    read
fi
if [[ $XDG_SESSION_TYPE == "x11" ]]; then
    echo 警告：你当前使用的是 x11 协议而非 Wayland 协议，Waydroid 只支持 Wayland 协议
    echo 按回车键忽略该警告继续安装Waydroid本体
    read
fi
rm -rf /tmp/gfdgd-xi-sources
mkdir -p /tmp/gfdgd-xi-sources
wget -P /tmp/gfdgd-xi-sources http://deb.waydroid.waydroid-runner.gfdgdxi.top/gpg.asc
wget -P /tmp/gfdgd-xi-sources http://deb.waydroid.waydroid-runner.gfdgdxi.top/sources/github.list
gpg --dearmor /tmp/gfdgd-xi-sources/gpg.asc
#sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FD6EEA1F20CD4B27
sudo cp -v /tmp/gfdgd-xi-sources/gpg.asc.gpg /etc/apt/trusted.gpg.d/gfdgdxi-list-waydroid.gpg
sudo cp -v /tmp/gfdgd-xi-sources/github.list /etc/apt/sources.list.d/gfdgdxi-list-waydroid.list
sudo apt update
sudo apt install waydroid -y
echo 安装完成！
read