#Please start waydroid session before running this Script!
#请不要以root身份执行!Do NOT Running by root!
import sys
import os
a = os.popen('waydroid status').readlines() #检查运行状态
if a[0].find('STOPPED')!=-1:
    print('-请先启动容器Session!')
    print('-程序出现异常,正在退出')
    sys.exit(1)
print('-正在关闭Waydroid窗口下多显示鼠标的功能:',end='')       #关闭Wayland窗口下显示鼠标功能
if os.system('waydroid prop set persist.waydroid.cursor_on_subsurface false')!=0:
    print('失败!\n-未知异常,程序即将退出!')
    sys.exit(1)
print('-成功!\n-重启容器生效!')
sys.exit(0)