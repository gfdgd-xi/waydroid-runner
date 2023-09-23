#!/usr/bin/env python3
#Please DO NOT RUNNING BY sudo!
import os
import sys
import subprocess
programPath = os.path.split(os.path.realpath(__file__))[0]  # 获取程序路径

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo 提权完成! && clear')
print('本程序将默认开启以下功能:')
print('1.开启多窗口模式')
print('2.默认防止屏幕旋转')
#print('3.设置语言为中文/简体')
print('3.Deepin-v23下显示Wayland的安卓窗口光标')
print('4.开启剪切板互通功能')
print('-建议使用Ubuntu等国际化Debian发行版')
print()

choose = input('-是否需要安装Magisk-Delta?是请输入y回车,不需要请直接回车:')      ##Magisk-Delta安装
if choose == 'y' or choose == 'Y':        
    print('-正在安装Magisk-Delta:',end="")
    if not subprocess.getstatusoutput(f'python3 "{programPath}/../Magisk_Installer/Magisk.py"')[0]:
        print('成功!')
    else:print('失败!请自行查找原因!')
else:print('-已跳过Magisk-Delta安装,如果您以后需要可以在Waydroid运行器里安装')

if subprocess.getstatusoutput('lsb_release -a')[0]:         ##检测系统版本,异常给os_release变量返回-1
    print('-运行部分异常,程序无法读取操作系统版本,请自行安装lsb_release组件!')
    os_release = -1
    flag_support = 0        #检测不到默认可以
else:
    os_release = subprocess.getstatusoutput('lsb_release -a')[1]
    flag_unsupport = 0              #检测系统,deepin 20和UOS要特殊配置
    if (os_release.find('deepin')!=-1 and os_release.find('20')!=-1) or os_release.find('UOS') != -1:
        flag_unsupport = 1

# 国内源的 Waydroid 已默认设置中文语言
#以下程序先执行不需要启动session的部分,然后再启动需要启动session的部分
#print('-正在设置语言为中文/简体:',end='')       #先设置语言
#if not subprocess.getstatusoutput(f'sudo python3 "{programPath}/../SystemConfigs/Language.py"')[0]:
#    print('成功!')
#else:print('失败,请自行排查问题!')

if flag_unsupport==1:   #剪切板先检测系统,再安装,目前不支持deepin 20/UOS
    print('-您的系统不支持剪切板互通,已跳过安装剪切板功能')
else:
    print('-正在开启剪切板支持:', end='')
    if os.system(f'python3 "{programPath}/../SystemConfigs/Clipboard-enable.py"') == 0:   #这里要用os.system(),这一步时间会比较长,需要用户能看得到输出内容!
        print('成功!\n')
    else:
        print('失败,请自行排查问题!\n')

###接下来启动Waydroid Session进行下一步配置
print('\n-正在重启Waydroid Container:', end='')         
if not subprocess.getstatusoutput('sudo systemctl restart waydroid-container.service')[0]:       ##先重启容器
    print('成功!')
else:print('失败,请自行排查问题!')

print('-正在启动Waydroid Session,耗时会比较长,请耐心等待(一般不超过6分钟)')
print('-正在等待启动Waydroid Session:',end='')  ###启动Waydroid Session
session=os.popen('waydroid session start')
while True:         #循环检测Waydroid session是否已启动
    WaydroidStatus = session.read()
    if WaydroidStatus.find('is ready') != -1:    ###检测session已经启动
        print('已检测启动!')
        break

if flag_unsupport == 1 or os.getenv("XDG_SESSION_TYPE") == "x11":   #多窗口先检测系统,再安装,目前不支持deepin 20/UOS以及使用x11协议的情况
    print('-检测到您使用不支持的系统/使用X11协议,已跳过多窗口模式开启功能')
else:
    print('-正在开启多窗口模式',end='')        #检测后应用多窗口模式
    if subprocess.getstatusoutput(f'python3 "{programPath}/../SystemConfigs/Multi_windows.py"')[0]==0:
        print('成功!')
    else:print('失败,请自行排查问题!')

print('-正在强制防止Waydroid内应用旋转:', end='')         #开启防旋转功能
if subprocess.getstatusoutput(f'python3 "{programPath}/../SystemConfigs/Do-not-rotate.py"')[0]==0:
    print('成功!')
else:print('失败,请自行排查问题!')

if os_release.find('deepin') != -1 and os_release.find('23') != -1 and os.getenv("XDG_SESSION_TYPE") == "x11":  ##Deepin v23修复不显示光标的问题
    print('-检测到您在使用deepin v23,正在修复Wayland安卓窗口下不显示光标的问题:',end='')
    if subprocess.getstatusoutput(f'python3 "{programPath}/../SystemConfigs/Show-cursor.py"')[0] == 0:
        print('成功!')
    else:print('失败,请自行排查问题!')

print()
print('Waydroid已自动配置完成,按回车键退出!')
input()
sys.exit(0)