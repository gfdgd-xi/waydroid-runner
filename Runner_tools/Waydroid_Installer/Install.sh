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
sudo apt install curl ca-certificates -y
curl https://repo.waydro.id | sudo bash
sudo apt install waydroid -y
echo Waydroid本体安装完成！按回车键退出！
read