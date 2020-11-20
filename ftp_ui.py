from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        self.log = ""
        self.text = "..\n"
        self.createFileListWidget()
        # self.fileList.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        # self.fileList.customContextMenuRequested.connect(self.showMenu)  # 绑定事件
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(718, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 0, 5, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.lineEdit_4, 2, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        # self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser.setObjectName("textBrowser")
        # self.gridLayout.addWidget(self.textBrowser, 6, 0, 1, 4)
        self.gridLayout.addWidget(self.fileList, 6, 4, 1, 4)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 6, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 2)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 4, 2, 1, 1)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 5, 4, 1, 1)

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 5, 5, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 5, 0, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 5, 2, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 718, 21))
        self.menubar.setObjectName("menubar")
        self.menueasyFTP = QtWidgets.QMenu(self.menubar)
        self.menueasyFTP.setObjectName("menueasyFTP")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menueasyFTP.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # 方便测试
        self.lineEdit.setText("public.sjtu.edu.cn")
        self.lineEdit_2.setText("ChinW66")
        self.lineEdit_3.setText("21")
        self.lineEdit_4.setText("public")
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "主机(H):"))
        self.label_3.setText(_translate("MainWindow", "密码:"))
        self.label_4.setText(_translate("MainWindow", "用户名:"))
        self.pushButton.setText(_translate("MainWindow", "快速连接"))
        self.label_2.setText(_translate("MainWindow", "端口(P):"))
        self.pushButton_2.setText(_translate("MainWindow", "新建文件夹"))
        self.pushButton_3.setText(_translate("MainWindow", "upload"))
        self.pushButton_4.setText(_translate("MainWindow", "关闭连接"))
        self.pushButton_5.setText(_translate("MainWindow", "download"))
        self.pushButton_6.setText(_translate("MainWindow", "重命名"))
        self.menueasyFTP.setTitle(_translate("MainWindow", "easyFTP"))
        self.menuhelp.setTitle(_translate("MainWindow", "help"))

        
    def showDialog(self):
        vbox=QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        panel = QtWidgets.QLabel()
        panel.setText("连接失败！请检查输入信息")
        self.dialog = QtWidgets.QDialog()
        self.dialog.resize(300,200)
        self.okBtn = QtWidgets.QPushButton("确定")
        self.cancelBtn = QtWidgets.QPushButton("返回")
        self.okBtn.clicked.connect(self.ok)
        self.cancelBtn.clicked.connect(self.cancel)
        self.dialog.setWindowTitle("提示信息！")
        hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancelBtn)
        vbox.addWidget(panel)
        vbox.addLayout(hbox)
        self.dialog.setLayout(vbox)
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog.exec_()
    def ok(self):
        self.dialog.close()
    def cancel(self):
        self.dialog.close()
    def callbacklog(self, msg):
        self.log =self.log +msg+ "\n"
        self.textBrowser_2.setText(self.log)
    # def filedir(self,filelist):
    #     if filelist==None:
    #         return
    #     for file in filelist:
    #         self.text =self.text+file+ "\n"
    #     self.textBrowser.setText(self.text)
    def createFileListWidget(self):
        self.fileList = QtWidgets.QTreeWidget()
        self.fileList.setIconSize(QtCore.QSize(20, 20))
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(('Name', 'Size', 'Owner', 'Group', 'Time', 'Mode'))
        self.fileList.header().setStretchLastSection(False)
    # def showMenu(self):
    #     item = self.fileList.currentItem()
    #     #item1 = self.fileList.itemAt(pos)
    #     menu = QMenu()
    #     download = menu.addAction(QAction(u'下载',self))
    #     # download.triggered.connect(self.testDownload)
    #     property = menu.addAction(QAction(u"属性",self))
    #     # property.triggered.connect(self.testProperty)
    #     menu.popup(QCursor.pos())
    #     print("++++++++++")
    def NewNameDialog(self):
        vbox=QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        line = QtWidgets.QLineEdit()
        line.setText("请输入名字")
        newnamedialog = QtWidgets.QDialog()
        newnamedialog.resize(400,300)
        okBtn = QtWidgets.QPushButton("确定")
        cancelBtn = QtWidgets.QPushButton("返回")
        okBtn.clicked.connect(self.ok)
        cancelBtn.clicked.connect(self.cancel)
        newnamedialog.setWindowTitle("提示信息！")
        hbox.addWidget(okBtn)
        hbox.addWidget(cancelBtn)
        vbox.addWidget(line)
        vbox.addLayout(hbox)
        newnamedialog.setLayout(vbox)
        newnamedialog.setWindowModality(QtCore.Qt.ApplicationModal)
        newnamedialog.exec_()
        return line.text()
    def testDownload(self):
        print("download success")
    def testProperty(self):
        print("testProperty success")


    
    