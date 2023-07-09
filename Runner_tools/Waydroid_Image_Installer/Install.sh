#!/bin/bash
echo 请输入版本代号（如focal、bullseye）
read VERSION
curl https://jihulab.com/gfdgd-xi/waydroid-deb/-/raw/main/$VERSION/Release
curl https://jihulab.com/gfdgd-xi/waydroid-deb/-/raw/main/$VERSION/Release | grep 404
if [[ $? != 0 ]]; then
    echo 不支持该版本代号
    exit 1
fi