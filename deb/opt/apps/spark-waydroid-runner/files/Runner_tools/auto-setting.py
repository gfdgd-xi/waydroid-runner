#!/usr/bin/env python3
import os
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
if os.system("which waydroid") >> 8:
    print("安装 Waydroid 主程序")
    os.system(f"bash '{programPath}/Waydroid_Installer/Install-cn.sh'")
os.system(f"bash '{programPath}/Waydroid_Image_Installer/Install.sh'")
os.system(f"sudo python3 '{programPath}/SystemConfigs/Language.py'")
os.system(f"sudo python3 '{programPath}/SystemConfigs/Multi_windows.py'")
os.system(f"python3 '{programPath}/SystemConfigs/Do-not-rotate.py'")
os.system(f"bash '{programPath}/Libhoudini_installer/Install.sh'")