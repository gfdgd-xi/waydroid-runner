#Please running by root!
#这个脚本很特殊,它需要用普通用户而不是sudo执行,但是程序执行时需要sudo,请特殊化处理
import os
import time
import sys
print('-重启容器服务\n')
os.system('sudo systemctl restart waydroid-container.service')
os.popen('waydroid session start')
time.sleep(35)
print('-正在应用设置')
os.system('sudo waydroid shell wm set-fix-to-user-rotation enabled')
print('-完成!')
sys.exit(0)
