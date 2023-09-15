#!/bin/bash

echo "###Waydroid一键配置程序###"
echo "本程序将安装Waydroid本体和GAPPS镜像"
echo ""
which waydroid
if [[ $? == 0 ]]; then
    echo Waydroid 已安装，是否重复安装？
    echo 是请按回车，否则按右上角 ×
    read
fi
sudo modprobe binder_linux
lsmod | grep -e binder_linux
if [[ $? != 0 ]] && [[ -f /dev/binder ]] && [[ -f /dev/binderfs ]]; then
    echo 您的内核似乎不支持 binder 模块，是否继续安装？安装完后可能无法使用
    echo 测试过可以使用的内核：https://gfdgdxi.lanzoue.com/b01r54ple    密码:35j0
    echo 按回车继续
    read
fi
x11=0
if [[ $XDG_SESSION_TYPE == "x11" ]]; then
    echo 警告：你当前使用的是 x11 协议而非 Wayland 协议，Waydroid 只支持 Wayland 协议
    echo 输入 Y 安装 Sway 或 Weston 以能在 X11 下运行 Waydroid（体验较差）
    x11=1
    read choose
    if [[ $choose == "Y" ]] || [[ $choose == "y" ]]; then
	echo Try to install sway
        cd `dirname $0`
        bash InstallSway.sh
        if [[ $? != 0 ]]; then
            echo Sway 安装失败，安装 Weston
            bash InstallWeston.sh
        fi
    fi
fi
# 检测 UEngine 是否安装
which uengine
if [[ $? == 0 ]]; then
    which uengine-loading-ubuntu
    if [[ $? == 0 ]]; then
        echo "Waydroid 与 UEngine 冲突，是否要先卸载 UEngine？[Y/N]"
        read choose
        if [[ $choose == "Y" ]] || [[ $choose == "y" ]]; then
            sudo apt purge uengine -y
            sudo apt purge uengine-modules-dkms uengine-android-image -y
            sudo apt-mark unhold hold lxc lxc-templates liblxc1 liblxc-common lxc-utils
            sudo apt update
            sudo apt install aptitude -y
            sudo aptitude install lxc -y
            sudo rm -v /usr/share/applications/uengine-loading-ubuntu.desktop
            sudo rm -v /etc/xdg/autostart/uengine-loading-ubuntu.desktop
            for username in $(ls /home)  
            do
                echo /home/$username
                sudo rm /home/$username/uengine-launch/run_daemon.sh
            done
            sudo rm -v /usr/bin/uengine-loading-binder
            sudo rm -v /usr/share/polkit-1/actions/com.deepin.pkexec.binder.loader.policy
        fi
    else
        echo "Waydroid 与 UEngine 冲突，是否要先卸载 UEngine？[Y/N]"
        read choose
        if [[ $choose == "Y" ]] || [[ $choose == "y" ]]; then
            sudo apt purge uengine -y
            sudo apt purge uengine-modules-dkms uengine-android-image -y
        fi
    fi
fi
rm -rf /tmp/gfdgd-xi-sources
mkdir -p /tmp/gfdgd-xi-sources
wget -P /tmp/gfdgd-xi-sources http://deb.waydroid.waydroid-runner.gfdgdxi.top/gpg.asc
wget -P /tmp/gfdgd-xi-sources http://deb.waydroid.waydroid-runner.gfdgdxi.top/sources/github.list
gpg --dearmor /tmp/gfdgd-xi-sources/gpg.asc
#sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FD6EEA1F20CD4B27
if [[ ! -f /etc/deepin_version ]] && [[ -f /etc/deepin-version ]]; then
    isDeepin=0
    lsb_release -i | grep -i deepin
    if [[ $? == 0 ]]; then
        isDeepin=1
    fi
    lsb_release -i | grep -i uos
    if [[ $? == 0 ]]; then
        isDeepin=1
    fi
    if [[ $isDeepin == 1 ]]; then
        echo 警告！
        echo 您当前使用的是 Deepin20.9/UOS，如果继续安装 Waydroid 则需要升级系统的 lxc，很可能出现问题，是否继续？
        echo 按回车继续
        read
        sudo bash -c 'echo "deb http://seafile.jyx2048.com:2345/waydroid-runner/lxc/ ./" > "/etc/apt/sources.list.d/gfdgdxi-list-lxc.list"'
    fi
fi
sudo cp -v /tmp/gfdgd-xi-sources/gpg.asc.gpg /etc/apt/trusted.gpg.d/gfdgdxi-list-waydroid.gpg
sudo cp -v /tmp/gfdgd-xi-sources/github.list /etc/apt/sources.list.d/gfdgdxi-list-waydroid.list
sudo apt update
sudo apt install waydroid lxc -y
sudo systemctl restart waydroid-container.service
sudo waydroid init -f
if [[ x11 == 1 ]]; then
    zenity --info "--text=Waydroid安装完成，在打开 Waydroid 前请先打开 Sway 或者 Weston 以便正常使用 Waydroid（目前支持自动调用）" --no-wrap
else
    zenity --info "--text=Waydroid安装完成！" --no-wrap
fi

echo 您已安装Waydroid,是否对其进行一些默认配置
echo 按回车键以进行配置
read
bash python3 Waydroid-AutoConfig.py
