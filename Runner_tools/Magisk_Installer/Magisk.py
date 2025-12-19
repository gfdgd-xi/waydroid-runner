#!/bin/env python3
# DO NOT Running this by ROOT!
import os
import sys
import time

# 定位到 data.img 所在目录以便脚本能正常调用
os.chdir(os.path.split(os.path.realpath(__file__))[0])

# 存储当前路径变量
cur_dir = os.getcwd()

# 设置必须变量
user = os.getlogin()   # 获取当前登录用户
waydroid_path = '/var/lib/waydroid' # 指定Waydroid本体路径
waydroid_data_mount = "/tmp/waydroid-runner-magisk-files-mount"
# Waydroid的用户data分区位置
waydroid_data_path = f'/home/{user}/.local/share/waydroid/data'
# 将Magisk修补二进制文件拷贝到用户data分区的具体目录
waydroid_magisk_files_in_data_path_linux = f'/home/{user}/.local/share/waydroid/data/media/magisk_tmp'
# 拷贝后Magisk文件在Waydroid系统内的路径地址
waydroid_magisk_files_in_data_path_android = '/data/media/magisk_tmp'


def Cleaner():   # 清理安装目录产生的Cache
    os.system(f'sudo rm -rf {waydroid_magisk_files_in_data_path_linux}')
    os.system(f'sudo umount {waydroid_data_mount} && sudo rm -r {waydroid_data_mount}')

#######--------------主程序部分----------------###########

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo -提权成功! && clear')
# 在/tmp重置工作目录
if os.path.exists(waydroid_data_mount) == False: os.system(f'sudo mkdir -p "{waydroid_data_mount}"')
print('-开始安装Magisk:')     
# 先检查文件完整性
if os.path.exists('data.img') == False: 
    print('-关键文件缺失!请重新安装运行器!')
    sys.exit(1)

# 挂载关键文件镜像（设置挂载只读）
os.system(f'sudo mount -o ro data.img {waydroid_data_mount}')

# 检测用户是否自行app里升级了Magisk-Delta
if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:
    print('-检测到您已经在app内安装过了Magisk,此脚本会进行重装操作')
    if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:
        # 清理旧版脚本的残留
        print('-正在删除残留的Magisk-Delta文件:',end='')
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/magisk')
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/init-delta.rc')
        print('完成')

    # 删除原来已安装过的Magisk残留
    os.system(f'sudo rm -rf {waydroid_path}/overlay_rw/system/system/etc/init/bootanim.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay_rw/system/system/etc/init/hw/init.zygote32.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay_rw/system/system/etc/init/hw/init.zygote64_32.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay_rw/vendor/etc/selinux/precompiled_sepolicy')
    os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/bootanim.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/hw/init.zygote32.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/hw/init.zygote64_32.rc')
    os.system(f'sudo rm -rf {waydroid_path}/overlay/vendor/etc/selinux/precompiled_sepolicy')

# 必须启动Waydroid,故启动前先检查其运行状态,若不在运行则进行启动
waydroid_status = os.popen('waydroid status').read()  #检查运行状态
if (waydroid_status!=-1): print('- 发现您未启动Waydroid,现在开始启动其服务')
os.popen('waydroid show-full-ui')

# 等待Waydroid完全启动
time.sleep(5)
while True:         # 循环检测Waydroid session是否已启动
    WaydroidStatus = os.popen('sudo waydroid shell getprop init.svc.bootanim').read()   # 使用Android Shell内部识别启动状态
    if WaydroidStatus.find('stopped') != -1: time.sleep(1)
    print('\n已检测Waydroid-session启动!')
    break
    
time.sleep(1)
# 预先新建系统分区待拷贝目录
# 复制Magisk文件同时到Overlay位置和data分区以便下一步修补vendor分区的SELinux policy
os.system(f'sudo mkdir -p {waydroid_magisk_files_in_data_path_linux} && sudo chmod 777 {waydroid_magisk_files_in_data_path_linux}')     # 预先新建用户分区待拷贝目录并设置权限
os.system(f'sudo mkdir -p /var/lib/waydroid/overlay/system/etc/init')
os.system(f'sudo mkdir -p /var/lib/waydroid/overlay/vendor/etc/selinux')

if os.system(f'sudo cp -a -f {waydroid_data_mount}/system/etc/init/* {waydroid_magisk_files_in_data_path_linux} && sudo chmod -R 777 {waydroid_magisk_files_in_data_path_linux}')==0: print('- 拷贝Magisk文件至用户分区完成')
else: print('- 拷贝文件至用户分区失败,请查找自身环境问题!')

if os.system(f'cd {waydroid_data_mount} && sudo cp patch_vendor_sepolicy.sh {waydroid_magisk_files_in_data_path_linux}')==0: print('- 拷贝SEPolicy修补脚本至用户分区完成')
else: print('- 拷贝修补脚本至用户分区失败,请查找自身环境问题!')

print('- 开始执行脚本修补SEPolicy:',end='')
os.system(f'sudo waydroid shell sh {waydroid_magisk_files_in_data_path_android}/patch_vendor_sepolicy.sh')
# 注意,执行这个脚本后会在/data/magisk_tmp下放置修补好的sepolicy文件
if (os.system(f'sudo cp {waydroid_magisk_files_in_data_path_linux}/precompiled_sepolicy {waydroid_path}/overlay/vendor/etc/selinux')==0): print('成功!')
else: print('失败,请自行排查问题!')
print()

# 修补完SEPolicy再将Magisk文件放至系统分区
if os.system(f'sudo cp -a -f {waydroid_data_mount}/system/etc/init/* {waydroid_path}/overlay/system/etc/init')==0: print('- 拷贝Magisk文件至系统分区完成')
else: print('- 拷贝文件至用户分区失败,请查找自身环境问题!')

print('- 已调用Waydroid安装Magisk应用本体')
os.system(f'waydroid app install {cur_dir}/app-release.apk')

print('- 正在清理目录')
Cleaner()

# 脚本收尾
print('- 安装完成,您可以重启Waydroid了!')
print('- 程序运行结束!')
sys.exit(0)
