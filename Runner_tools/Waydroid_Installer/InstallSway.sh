#!/bin/bash
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
    exit
fi
if [[ -f /etc/deepin_version ]]; then
    cat /etc/deepin_version | grep 23
    if [[ $? == 0 ]]; then
        # 加 apt 源
        which aptss
        if [[ $? == 0 ]]; then
            sudo aptss update
            sudo aptss install better-deepin23-source -y
        else
            aria2c -x 16 -s 16 https://zunyun01.store.deepinos.org.cn/store/depends/better-deepin23-source/better-deepin23-source_1.0_all.deb -d /tmp
            sudo apt install ./better-deepin23-source_1.0_all.deb
        fi
        sudo apt update
        sudo apt install sway -y
    fi
fi
echo 该系统暂时无法安装 Sway！
exit 1