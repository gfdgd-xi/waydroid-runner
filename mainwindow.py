#!/usr/bin/env python3
import sys
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
mainwindow = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
mainwindow.setWindowTitle("Waydroid 运行器")
mainwindow.setCentralWidget(widget)
mainwindow.show()
sys.exit(app.exec_())