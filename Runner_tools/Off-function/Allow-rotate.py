#Please start waydroid session before running this Script!
#Please running by root!

import os
import sys

a = os.popen('waydroid status').read()  #检查运行状态
if a.find('STOPPED')!=-1:
    print('-请先启动容器Session!')
    print('-程序出现异常,正在退出')
    sys.exit(1)

print('-正在设置允许应用旋转屏幕')
os.system('sudo waydroid shell wm set-fix-to-user-rotation disabled')
print('-完成!')
sys.exit(0)
