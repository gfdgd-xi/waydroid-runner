#!/usr/bin/env python3
import sys
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
mainwindow = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()
### 创建控件
## 安装 apk
apkPath = QtWidgets.QComboBox()
installButton = QtWidgets.QPushButton("安装")
# 设置属性
apkPath.setEditable(True)
# layout
apkInstallLayout = QtWidgets.QHBoxLayout()
apkInstallLayout.addWidget(apkPath)
apkInstallLayout.addWidget(installButton)
## info
gpuDevice = QtWidgets.QLabel("当前工作GPU：AMD Raven Ridge")
gpuChooser = QtWidgets.QPushButton("选择")
waydroidStatus = QtWidgets.QLabel("Waydroid：已安装")
magiskDeltoInstallStatus = QtWidgets.QLabel("Magisk Delto：已安装")
libkoudiniInstallStatus = QtWidgets.QLabel("Libkoudini：已安装")
lsPosedInstallStatus = QtWidgets.QLabel("LSPased：已安装")
diskUsing = QtWidgets.QLabel("存储占用：8.56GB")
memoryUsing = QtWidgets.QLabel("内存占用：850MB")
# layout
infoLayout = QtWidgets.QGridLayout()
infoLayout.addWidget(gpuDevice, 0, 0, 1, 2)
infoLayout.addWidget(gpuChooser, 0, 3)
infoLayout.addWidget(magiskDeltoInstallStatus, 1, 0)
infoLayout.addWidget(libkoudiniInstallStatus, 2, 0)
infoLayout.addWidget(diskUsing, 2, 1)
infoLayout.addWidget(lsPosedInstallStatus, 3, 0)
infoLayout.addWidget(memoryUsing, 3, 1)

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
configMenu = menu.addMenu("配置(&C)")
settingMenu = menu.addMenu("设置(&S)")
helpMenu = menu.addMenu("帮助(&H)")
# 程序栏
exitProgramAction = QtWidgets.QAction("退出程序")
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
sys.exit(app.exec_())