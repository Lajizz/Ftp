import socket
import os,sys
import ftplib
from ftplib import FTP
import ftp_ui
from ftp_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial
from ftplib import error_perm


# host  = 'public.sjtu.edu.cn'
# port  = 21
# ftp = FTP()
# ftp.set_debuglevel(2)
# user = "ChinW66"
# pw = "public"
# s = ftp.connect(host = host,port = port)
# print(ftp.welcome)
# ftp.login(user=user,passwd=pw)
ftp = FTP()
ftp.set_debuglevel(2)
curr_dir = '/upload'
def connect(ftp,ui):
    host = ui.lineEdit.text()
    port = int(ui.lineEdit_3.text())
    user = ui.lineEdit_2.text()
    passwd = ui.lineEdit_4.text()
    try:
        s = ftp.connect(host = host,port = port)
        ui.callbacklog(ftp.welcome)
        ftp.login(user=user,passwd=passwd)
        dir = cat_dir(ftp,filepath='/')
        ftp.cwd(curr_dir)
        ui.filedir(dir)
    except(socket.error, socket.gaierror):
        ui.showDialog()
        ui.callbacklog("failure connected")
    except error_perm:
        ui.showDialog()
        ui.callbacklog("failure authentication")
# dir = cat_dir(ftp,filepath='/')
# print(dir)
def cat_dir(ftp,filepath):
    cat = ftp.nlst(filepath)
    print("------------------")
    print(cat)
    return cat

def closeftp(ftp):
    ftp.close()
    print("close test")

def is_ftp_file(ftp, ftp_path):
    try:
        if ftp_path in ftp.nlst(os.path.dirname(ftp_path)):
            return True
        else:
            return False
    except error_perm:
        return False

def uploadfile(ftp,localpath,ui):
    bufsize = 1024
    fp = open(localpath, 'rb')
    res = ftp.storbinary('STOR ' + curr_dir, fp, bufsize)  # 上传文件
    if res.find('226') != -1:
        ('upload file complete', curr_dir)
    ftp.set_debuglevel(0)

# for test
def click_success():
    print("success")
def open_file():
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件", os.getcwd(), 
        "All Files(*);;Text Files(*.txt)")
if  __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ftp_ui.Ui_MainWindow()
    
    ui.setupUi(MainWindow)
    # 前端与后端相连接
    ui.pushButton.clicked.connect(partial(connect,ftp,ui))
    ui.pushButton_3.clicked.connect(open_file)
    MainWindow.show()
    
    sys.exit(app.exec_())
    
