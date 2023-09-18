#Python3 Program
#不要使用sudo/root用户执行!DO NOT RUNNING BY ROOT!
#请在Session运行时执行此脚本!Please while session running,then running the Script!

import os            #关键引用
import sys

print('如果你使用GNOME/KDE的DE,请不要执行这个脚本,否则会多显示一个鼠标!')        #温馨提示
a = os.popen('waydroid status').read() #检查运行状态
if a.find('STOPPED')!=-1:
    print('-请先启动容器Session!')
    print('-程序出现异常,正在退出')
    sys.exit(1)

print('-正在设置启动Waydroid后会多留一个鼠标')           #开启功能
if os.system('waydroid prop set persist.waydroid.cursor_on_subsurface true')!=0:
    print('失败!\n-未知异常,程序即将退出!')
    sys.exit(1)
print('成功!重启Waydroid后生效!')
sys.exit(0)
