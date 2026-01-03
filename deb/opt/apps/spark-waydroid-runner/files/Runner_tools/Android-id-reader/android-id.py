#!/bin/env python3
#A python3 program
#Please DO-NOT-RUNNING by root!
import os
import sys
os.chdir(os.path.split(os.path.realpath(__file__))[0]) # 定位到gms.py所在目录以便脚本能正常调用

print('-请在下方输入您的sudo密码')     #提权,软件后期运行需要sudo,但是又要正确识别当前用户
os.system('sudo echo "-提权成功!"')
os.system('clear')

a = os.popen('waydroid status').read()    #检查Session运行状态,需要使用Waydroid-shell
if a.find('STOPPED')!=-1:
    print('-请先启动容器Session!')
    print('-程序出现异常,正在退出')
    sys.exit(1)

user=os.getlogin()   #获取当前用户名
waydroid_data='/home/'+user+'/.local/share/waydroid/data'

print('-复制gms.sh脚本到安卓目录:',end='')
if os.system(f'sudo cp gms.sh {waydroid_data}/media/0')!=0:
    print('失败!请自行查找问题!');sys.exit(1)   #复制gms.sh文件,设定权限,这个gms.sh要在Android-shell跑
else:print('完成!')
print('-设置脚本权限:')
if os.system(f'sudo chmod 777 {waydroid_data}/media/0/gms.sh')!=0:
    print('失败!请自行查找问题!');sys.exit(1)   #复制gms.sh文件,设定权限,这个gms.sh要在Android-shell跑
else:print('完成!')


android_id=os.popen('sudo waydroid shell sh /sdcard/gms.sh').read()    #执行脚本,拿到输出的Android-id
#清理残留目录
os.system('sudo waydroid shell rm /sdcard/gms.sh')
if android_id.find('android_id')==-1:
    print('\n-未找到Android id!')
    print('-请在本帖子查看详细信息:https://bbs.deepin.org/post/261685')
else:
    android_id=android_id[android_id.find('android_id'):]                 #获取安卓id,去掉不必要的信息
    print('\n下方为您的Android-id(调用安卓内输出,注册时只需要复制对应数字输入即可)')
    print(android_id)

a=input('-请按回车或者输入任意键退出')
sys.exit(0)
