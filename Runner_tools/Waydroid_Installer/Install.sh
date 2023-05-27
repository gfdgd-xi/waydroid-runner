#!/bin/bash
if [[ $XDG_SESSION_TYPE == "x11" ]]; then
    echo 警告：你当前使用的是 x11 协议而非 Wayland 协议，Waydroid 只支持 Wayland 协议
    echo 按回车键忽略该警告继续安装
    read
fi
sudo apt install curl ca-certificates -y
curl https://repo.waydro.id | sudo bash
sudo apt install waydroid -y
echo 安装完成！按回车键退出！
read