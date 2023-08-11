#!/usr/bin/env python3
import os
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
if os.system("which waydroid") >> 8:
    print('-您还没有安装Waydroid主程序，现在为您安装')
    print("-安装 Waydroid 主程序")
    os.system(f"bash '{programPath}/Waydroid_Installer/Install-cn.sh'")
print('自动设置将设置以下内容:1.语言设置为中文-简体 2.安装Libhoudini 3.开启多窗口模式 4.防止意外旋转')
print('-正在下载Waydroid Images')
os.system(f"bash '{programPath}/Waydroid_Image_Installer/Install.sh'")
print('-正在设置语言')
os.system(f"sudo python3 '{programPath}/SystemConfigs/Language.py'")
a = os.popen('waydroid session start').read()
while a.find('ready')!=-1:
    print('-正在开启多窗口')
    os.system(f"sudo python3 '{programPath}/SystemConfigs/Multi_windows.py'")
    print('-正在防意外旋转')
    os.system(f"python3 '{programPath}/SystemConfigs/Do-not-rotate.py'")
print('-正在重启容器')
os.system('sudo systemctl restart waydroid-container.service')
print('-如您有Magisk需要,可在运行器里安装~')