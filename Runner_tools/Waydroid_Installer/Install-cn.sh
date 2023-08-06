#!/bin/bash
sudo modprobe binder_linux
lsmod | grep -e binder_linux
if [[ $? != 0 ]] && [[ -f /dev/binder ]] && [[ -f /dev/binderfs ]]; then
    echo 您的内核似乎不支持 binder 模块，是否继续安装？安装完后可能无法使用
    echo 按回车继续
    read
fi
x11=0
if [[ $XDG_SESSION_TYPE == "x11" ]]; then
    echo 警告：你当前使用的是 x11 协议而非 Wayland 协议，Waydroid 只支持 Wayland 协议
    echo 输入 Y 安装 Sway 或 Weston 以能在 X11 下运行 Waydroid
    x11=1
    read choose
    if [[ choose == "Y" ]]; then
        cd `dirname $1`
        bash InstallSway.sh
        if [[ $? != 0 ]]; then
            echo Sway 安装失败，安装 Weston
            bash InstallWeston.sh
        fi
    fi
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
sudo systemctl restart waydroid-container.service
sudo waydroid init -f
