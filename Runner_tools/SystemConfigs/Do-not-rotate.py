#Please start waydroid session before running this Script!
#Please running by root!
#这个脚本很特殊,它需要用普通用户而不是sudo执行,但是程序执行时需要sudo,请特殊化处理
import os
import time
import sys

print('-正在应用设置')
os.system('sudo waydroid shell wm set-fix-to-user-rotation enabled')
print('-完成!')
sys.exit(0)
