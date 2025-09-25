#!/bin/env python3
import os
import sys

# 定位到 data.img 所在目录以便脚本能正常调用
os.chdir(os.path.split(os.path.realpath(__file__))[0])

# 设置必须变量
waydroid_path = '/var/lib/waydroid' # 指定Waydroid本体路径
waydroid_data_mount = "/tmp/waydroid-runner-magisk-files-mount"
user = os.getlogin()   # 获取当前登录用户

def Cleaner():   # 清理安装目录产生的Cache
    print('-正在清理目录:',end='')
    os.system(f'sudo umount "{waydroid_data_mount}" && sudo rm -rf "{waydroid_data_mount}"')
    print('完成')

#######--------------主程序部分----------------###########

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo -提权成功! && clear')
if os.path.exists(waydroid_data_mount) == False:     # 在/tmp创建Cache
    os.system(f'sudo mkdir "{waydroid_data_mount}"')
print('-开始安装Magisk-delta')     
if os.path.exists('data.img') == False:          # 检查文件完整性
    print('-关键文件缺失!请重新安装运行器!')
    sys.exit(1)
os.system(f'sudo mount -o ro data.img "{waydroid_data_mount}"')          # 挂载关键文件镜像（设置挂载只读）

if os.path.exists(f'{waydroid_path}/overlay_rw/system/system/etc/init/magisk') == True:         # 检测用户是否自行app里升级了Magisk-Delta
    print('-检测到您已经在app内安装过了Magisk-Delta,此脚本不会执行任何升级操作')
    if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:            # 检测是否有旧版残留,有就删掉
        print('-正在删除残留的Magisk-Delta文件:',end='')
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/magisk')            # 清理旧版脚本的残留
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/init-delta.rc')            # 清理旧版脚本的残留
        print('完成')
    print('- 此后只需在Magisk-Delta的app里直接升级Magisk-Delta即可')
    Cleaner()
    print('\n程序运行结束!')
    sys.exit(0)
else:            # 若没检测到用户自行升级了Magisk
    if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:      # 但是发现旧版脚本安装残留,那么删掉残留
        print('- 检测到旧版Magisk文件残留,正在去除:',end='')
        if os.system('sudo rm -rf /var/lib/waydroid/overlay/system/etc/init/magisk.rc') == 0 and os.system('sudo rm -rf /var/lib/waydroid/overlay/system/etc/init/magisk') == 0: print('成功!')
        else: print('失败!请自行排查问题!')

    # 复制Magisk文件同时到Overlay_rw分区和data分区以便下一步修补vendor分区的SELinux policy
    os.system(f'sudo mkdir -p /var/lib/waydroid/overlay_rw/system/system/etc/init')     # 预先新建系统分区待拷贝目录
    os.system(f'sudo mkdir -p /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp && sudo chmod 777 /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp')     # 预先新建用户分区待拷贝目录并设置权限

    if os.system(f'cd "{waydroid_data_mount}/system/etc/init" && sudo cp -a -f * "{waydroid_path}/overlay_rw/system/system/etc/init" && sudo cp -a * /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp && cd /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp && sudo chmod -R 777 *')==0: print('- 拷贝Magisk文件至用户分区完成')
    else: print('- 拷贝文件至系统分区失败,请查找自身环境问题!')

    if os.system(f'cd {waydroid_data_mount} && sudo cp patch_vendor_sepolicy.sh /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp')==0: print('- 拷贝Magisk文件至用户分区完成')
    else: print('- 拷贝修补脚本至用户分区失败,请查找自身环境问题!')

    print('- 开始执行脚本修补SEPolicy:',end='')
    os.system(f'sudo waydroid shell sh /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp/patch_vendor_sepolicy.sh')
    # 注意,执行这个脚本后会在/data/magisk_tmp下放置修补好的sepolicy文件
    if (os.system(f'sudo cp /home/{user}/.local/share/waydroid/data/magisk_tmp/precompiled_sepolicy /{waydroid_path}/overlay_rw/vendor/etc/selinux')==0): print('成功!')
    else: print('失败,请自行排查问题!')
    print()

    print('- 正在清理目录',end='')
    os.system(f'sudo rm -rf /home/{user}/.local/share/waydroid/data/media/0/magisk_tmp && sudo rm -rf /home/{user}/.local/share/waydroid/data/magisk_tmp')

    print('- 安装完成!')
    Cleaner()       # 清理目录
    print('\n程序运行结束!')
    sys.exit(0)
