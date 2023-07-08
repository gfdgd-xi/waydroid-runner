#Please running by root!
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
