#!/usr/bin/env python3
import os
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
if os.system("which waydroid") >> 8:
    print("-安装 Waydroid 主程序")
    os.system(f"bash '{programPath}/Waydroid_Installer/Install-cn.sh'")
print('-正在下载Waydroid Images')
os.system(f"bash '{programPath}/Waydroid_Image_Installer/Install.sh'")
print('-正在设置语言')
os.system(f"sudo python3 '{programPath}/SystemConfigs/Language.py'")
print('-正在开启多窗口')
os.system(f"sudo python3 '{programPath}/SystemConfigs/Multi_windows.py'")
print('-正在防意外旋转')
os.system(f"python3 '{programPath}/SystemConfigs/Do-not-rotate.py'")
print('-正在安装Libhoudini')
os.system(f"bash '{programPath}/Libhoudini_installer/Install.sh'")
print('-正在重启容器')
os.system('sudo systemctl restart waydroid-container.service')
print('-如您有Magisk需要,可在运行器里安装~')