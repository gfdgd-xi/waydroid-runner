#!/bin/python3
#Please DO NOT RUNNING BY sudo!
import os
import sys
import subprocess
os.chdir(os.path.split(os.path.realpath(__file__))[0]  #定位到当前运行目录

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo 提权完成! && clear')
print('本程序将默认开启以下功能:')
print('-建议使用Ubuntu')
print('1.开启多窗口模式')
print('2.默认防止屏幕旋转')
print('3.设置语言为中文/简体')
print('4.Deepin-v23下显示Wayland的安卓窗口光标')
print('5.开启剪切板互通功能\n')

a=input('-是否需要安装Magisk-Delta?是请输入y回车,不需要请直接回车:')      ##Magisk-Delta安装
if a=='y' or a=='Y':        
    print('-正在安装Magisk-Delta:',end="")
    if subprocess.getstatusoutput('cd ../Magisk_Installer && python3 Magisk.py')[0] == '0':
        print('成功!')
    else:print('失败!请自行查找原因!')
else:print('-已跳过Magisk-Delta安装,如果您以后需要可以在Waydroid运行器里安装')

if subprocess.getstatusoutput('lsb_release -a')[0]!=0:         ##检测系统版本,异常给os_release变量返回-1
    print('-运行部分异常,程序无法读取操作系统版本,请自行安装lsb_release组件!')
    os_release=-1
else:
    os_release=subprocess.getstatusoutput('lsb_release -a')[1]

#以下程序先执行不需要启动session的部分,然后再启动需要启动session的部分
print('-正在设置语言为中文/简体',end='')       #先设置语言
if subprocess.getstatusoutput('python3 ../SystemConfigs/Language.py')[0]==0:
    print('成功!')
else:print('失败,请自行排查问题!')

if (os_release.find('deepin')!=-1 and os_release.find('20')!=-1) or os_release.find('UOS')!=-1:   #剪切板先检测系统,再安装,目前不支持deepin 20/UOS
    print('-您的系统不支持剪切板互通,已跳过安装剪切板功能')
else:
    print('-正在开启剪切板支持:',end='')
    if subprocess.getstatusoutput('python3 ../SystemConfigs/Clipboard-enable.py')==0:
        print('成功!')
    else:
        print('失败,请自行排查问题!')

###接下来启动Waydroid Session进行下一步配置
print('\n-正在重启Waydroid Container:',end='')         
if subprocess.getstatusoutput('sudo systemctl restart waydroid-container.service')[0]==0:       ##先重启容器
    print('成功!')
else:print('失败,请自行排查问题!')

print('-正在启动Waydroid Session,耗时会比较长,请耐心等待(一般不超过6分钟)')
print('-正在等待启动Waydroid Session:',end='')  ###启动Waydroid Session
subprocess.getstatusoutput('waydroid session start')
while True:
    WaydroidStatus=os.popen('waydroid status')
    if WaydroidStatus.find('ready')!=-1:    ###检测session已经启动
        print('已检测启动!')
        break

if ((os_release.find('deepin')!=-1 and os_release.find('20')!=-1) or os_release.find('UOS')!=-1) or os.popen('echo $XDG_SESSION_TYPE').read().find('x11'):   #多窗口先检测系统,再安装,目前不支持deepin 20/UOS

