# Waydroid运行器
## 介绍
Waydroid运行器是可以通过GUI形式半自动配置Waydroid的工具，使用户使用Waydroid更为方便。Waydroid本身存在很多因AOSP未考虑PC用户而产生的问题(如没有自带Houdini,默认英语,默认非小窗模式)而使用户使用起来非常难受,本运行器支持以GUI形式自动化安装以及配置Waydroid，并会创建快捷控制的快捷方式，可以用于玩游戏/刷视频/Android开发等。  


## 配置要求
仅限启用 Wayland 的 x86-64 的 Linux，ARM64的在安装Magisk时需要重新制作data.img(教程有时间放出来) 显卡仅限Intel & AMD(独立显卡需要启动桌面环境时使用独立显卡,否则无法使用),只有英伟达显卡(连Intel核心显卡都没有的)当前无法使用本项目，建议使用xDroid/UEngine作为替代。  
lxc 过老的系统（如 Debian10、Deepin 20.9）也无法正常运行 Waydroid  

## 安装&使用教程
下载安装本软件,然后按照提示执行即可  

## 历史版本
### 1.0.0（？？？？年？？月？？日）
**※1、新增 Waydroid 主程序安装功能、镜像下载功能及其国内源**  
**※2、支持安装 Magisk、Libhoudini（二进制翻译器，可以运行 ARM APK）**  
**※3、支持对 Waydroid 的初步控制**  
**※4、支持安装/卸载 Android 应用**  
**※5、提供应用商店以安装 APK**  

## 源码安装教程
```bash
git clone https://gitee.com/gfdgd-xi/waydroid-runner
cd waydroid-runner 
make install -j4
```

## 参与贡献
@Telegram HuskyDG 巨佬贡献的 `Magisk` 安装到 `/system` 分区的方案和他的 `Magisk-Delta`
@casualsuek 的 `Waydroid-Script` 亿点代码  

## ©2023~Now