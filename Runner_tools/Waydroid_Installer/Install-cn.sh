#!/bin/bash
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