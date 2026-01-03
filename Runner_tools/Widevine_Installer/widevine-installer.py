#!/bin/env python3
#Python3-Program
#目前仅支持安卓11
#Please runnning by root/sudo!
#如果您是龙芯处理器,请模拟架构为waydroid内的架构再运行本程序!
import os
import sys

# 定位到 widevine 镜像文件所在目录以便脚本能正常调用
os.chdir(os.path.split(os.path.realpath(__file__))[0])

# 存储当前路径变量
cur_dir = os.getcwd()

waydroid_widevine_mount_dir = "/tmp/waydroid-runner-widevinemount"
waydroid_overlay_dir = "/var/lib/waydroid/overlay"

print('- 请在下方输入您当前的管理员用户密码:')
os.system('sudo echo -提权成功! && clear')

# 检查目标目录权限
if os.system(f'sudo rm -rf {waydroid_widevine_mount_dir} && sudo mkdir {waydroid_widevine_mount_dir}')!=0:   #创建文件夹检查
	print('- 居然/tmp下无法创建文件夹,请自行排查问题!')
	print('- 程序即将退出')
	sys.exit(1)

# 检查系统架构
arch = os.popen('arch').read()
if arch.find('x86_64')!=-1:
	print('- 系统架构:x86_64')
	arch='x86_64'
elif arch.find('aarch64')!=-1:
	print('- 系统架构:arm64')
	print('- 不支持此架构!程序即将退出')
	arch='aarch64'
	sys.exit(1)
else:
    print(f'-系统架构:{arch}')
    print('- 不支持此架构!程序即将退出')

# 输出信息
print('- 开始安装Widevine')

# 检查文件自身完整性
if os.path.exists(f'{cur_dir}/widevine-{arch}-13.img')==False:
	print('- 警告:关键文件缺失!')
	print('- 程序即将退出')
	sys.exit(1)

if (os.system(f'sudo mount {cur_dir}/widevine-{arch}-13.img {waydroid_widevine_mount_dir}')!=0):
    print('- 挂载失败!')
    sys.exit(1)

# 清理旧目录残余
print('- 正在清理旧目录:', end='')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/bin/hw/android.hardware.drm@1.4-service-lazy.widevine')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/bin/move_widevine_data.sh')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/etc/init/android.hardware.drm@1.4-service-lazy.widevine.rc')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/etc/vintf/manifest/manifest_android.hardware.drm@1.4-service.widevine.xml')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/lib/libprotobuf-cpp-full-3.9.1.so')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/lib/libprotobuf-cpp-lite-3.9.1.so')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/lib64/libprotobuf-cpp-full-3.9.1.so')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/lib64/libprotobuf-cpp-lite-3.9.1.so')
os.system(f'sudo rm -rf {waydroid_overlay_dir}/vendor/lib64/libwvhidl.so')
print('完成!')


# 创建必须文件夹
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/bin')
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/bin/hw')
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/etc/init')
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/etc/vintf/manifest')
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/lib')
os.system(f'sudo mkdir -p {waydroid_overlay_dir}/vendor/lib64')
# 复制文件到Overlay
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/bin/hw/* {waydroid_overlay_dir}/vendor/bin/hw')
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/bin/move_widevine_data.sh {waydroid_overlay_dir}/vendor/bin')
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/etc/init/* {waydroid_overlay_dir}/vendor/etc/init')
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/etc/vintf/* {waydroid_overlay_dir}/vendor/etc/vintf')
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/lib/* {waydroid_overlay_dir}/vendor/lib')
os.system(f'sudo cp -a -f {waydroid_widevine_mount_dir}/lib64/* {waydroid_overlay_dir}/vendor/lib64')

# 结尾
print('-安装完成!')
os.system(f'cd ~ && sudo umount {waydroid_widevine_mount_dir} && sudo rm -rf {waydroid_widevine_mount_dir}')
sys.exit(0)
