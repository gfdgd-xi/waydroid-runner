#Python3-Program
import os
import sys
os.chdir(os.path.split(os.path.realpath(__file__))[0]) # 定位到 data.img 所在目录以便脚本能正常调用
waydroid_path = '/var/lib/waydroid'
waydroid_data_mount = "/tmp/waydroid-runner-datamount"
def Cleaner():   #清理安装目录产生的Cache
    print('-正在清理目录:',end='')
    os.system(f'sudo umount "{waydroid_data_mount}" && sudo rm -rf "{waydroid_data_mount}"')
    print('-完成')

#######--------------主程序部分----------------###########

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo -提权成功! && clear')
if os.path.exists(waydroid_data_mount) == False:     #在/tmp创建Cache
    os.system(f'sudo mkdir "{waydroid_data_mount}"')
print('-开始安装Magisk-delta')     
if os.path.exists('data.img') == False:          #检查文件完整性
    print('-关键文件缺失!请重新安装运行器!')
    sys.exit(1)
os.system(f'sudo mount -o ro data.img "{waydroid_data_mount}"')          #挂载关键文件镜像（设置挂载只读）

if os.path.exists(f'{waydroid_path}/overlay_rw/system/system/etc/init/magisk') == True:         #检测用户是否自行app里升级了Magisk-Delta
    print('-检测到您已经在app内安装过了Magisk-Delta,此脚本不会执行任何升级操作')
    if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:            #检测是否有旧版残留,有就删掉
        print('-正在删除残留的Magisk-Delta文件:',end='')
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/magisk')            #清理旧版脚本的残留
        os.system(f'sudo rm -rf {waydroid_path}/overlay/system/etc/init/init-delta.rc')            #清理旧版脚本的残留
        print('完成')
    print('-此后只需在Magisk-Delta的app里直接升级Magisk-Delta即可')
    Cleaner()
    print('\n程序运行结束!')
    sys.exit(0)
else:            #若没检测到用户自行升级了Magisk-Delta
    if os.path.exists(f'{waydroid_path}/overlay/system/etc/init/magisk') == True:      #但是发现旧版脚本安装残留,那么删掉残留
        print('-检测到旧版Magisk文件残留,正在去除:',end='')
        if os.system('sudo rm -rf /var/lib/waydroid/overlay/system/etc/init/magisk.rc') == 0 and os.system('sudo rm -rf /var/lib/waydroid/overlay/system/etc/init/magisk') == 0:print('成功!')
        else:print('失败!请自行排查问题!')
    os.system(f'sudo mkdir -p /var/lib/waydroid/overlay_rw/system/system/etc/init')  #复制data.img中文件到新Overlay_rw
    os.system(f'cd "{waydroid_data_mount}/system/etc/init" && sudo cp -rf * "{waydroid_path}/overlay_rw/system/system/etc/init"')
    print('-安装完成!')
    Cleaner()       #清理目录
    print('\n程序运行结束!')
    sys.exit(0)
