#!/usr/bin/env python3
# 基于 GPLV3 开源
import os
import sys
#from torch import *
import torch
#import pynvml
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
mainwindow = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()
### 创建控件
## 安装 apk
apkPath = QtWidgets.QComboBox()
apkPathBrowser = QtWidgets.QPushButton("浏览")
installButton = QtWidgets.QPushButton("安装")
# 设置属性
apkPath.setEditable(True)
# layout
apkInstallLayout = QtWidgets.QHBoxLayout()
apkInstallLayout.addWidget(apkPath)
apkInstallLayout.addWidget(apkPathBrowser)
apkInstallLayout.addWidget(installButton)
## info
gpuDevice = QtWidgets.QLabel("当前工作GPU：AMD Raven Ridge")
gpuChooser = QtWidgets.QPushButton("选择")
waydroidStatus = QtWidgets.QLabel("Waydroid：已安装")
magiskDeltoInstallStatus = QtWidgets.QLabel("Magisk Delta：已安装")
libkoudiniInstallStatus = QtWidgets.QLabel("Libhoudini：已安装")
lsPosedInstallStatus = QtWidgets.QLabel("LSPosed：已安装")
diskUsing = QtWidgets.QLabel("存储占用：8.56GB")
memoryUsing = QtWidgets.QLabel("内存占用：850MB")
# layout
infoLayout = QtWidgets.QGridLayout()
infoLayout.addWidget(waydroidStatus, 0, 0, 1, 2)
infoLayout.addWidget(gpuDevice, 1, 0, 1, 2)
infoLayout.addWidget(gpuChooser, 1, 3)
infoLayout.addWidget(magiskDeltoInstallStatus, 2, 0)
infoLayout.addWidget(libkoudiniInstallStatus, 3, 0)
infoLayout.addWidget(diskUsing, 3, 1)
infoLayout.addWidget(lsPosedInstallStatus, 4, 0)
infoLayout.addWidget(memoryUsing, 4, 1)

## 大 layout
widgetLayout.addLayout(apkInstallLayout, 2, 0)
widgetLayout.addLayout(infoLayout, 3, 0)

widget.setLayout(widgetLayout)
mainwindow.setWindowTitle("Waydroid 运行器 1.0.0")
mainwindow.setCentralWidget(widget)
## 菜单栏
menu = mainwindow.menuBar()
programMenu = menu.addMenu("程序(&W)")
waydroidMenu = menu.addMenu("Waydroid(&W)")
configMenu = menu.addMenu("容器配置(&C)")
helpMenu = menu.addMenu("帮助(&H)")
# 程序栏
settingProgramAction = QtWidgets.QAction("设置程序")
exitProgramAction = QtWidgets.QAction("退出程序")
programMenu.addAction(settingProgramAction)
programMenu.addAction(exitProgramAction)
exitProgramAction.triggered.connect(sys.exit)
# Waydroid 栏
gpuChooseAction = QtWidgets.QAction("GPU 选择")
waydroidMenu.addAction(gpuChooseAction)
# 帮助 栏
helpAction = QtWidgets.QAction("程序帮助")
uploadBugAction = QtWidgets.QAction("问题反馈")
aboutThisProgramAction = QtWidgets.QAction("关于本程序(&A)")
helpMenu.addAction(helpAction)
helpMenu.addAction(uploadBugAction)
helpMenu.addAction(aboutThisProgramAction)

## 窗口属性
# 图标待定
# mainwindow.setWindowIcon("")
mainwindow.show()

# 检测显卡型号
ng = torch.cuda.device_count()
print("Devices:%d" %ng)
infos = [torch.cuda.get_device_properties(i) for i in range(ng)]
print(infos)
#print(pynvml.nvmlDeviceGetCount())
#gpuDevice.setText(f"GPU 型号：{pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))}")
#deviceCount = pynvml.nvmlDeviceGetCount()

# 检测 Waydroid 是否存在
if os.system("which waydroid"):
    waydroidStatus.setText("Waydroid：未安装")


sys.exit(app.exec_())