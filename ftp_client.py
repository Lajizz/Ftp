import socket
import os,sys
import ftplib
from ftplib import FTP
import ftp_ui
from ftp_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from ftplib import error_perm

app_icon_path = os.path.join(os.path.dirname(__file__), 'icon')
qIcon = lambda name: QtGui.QIcon(os.path.join(app_icon_path, name))
ftp = FTP()
ftp.status = False
ftp.set_debuglevel(0)
back_dir = ['/']
remote_dir = '/'
remoteFilelist = []
remoteDir = {}
def connect(ftp,ui):
    host = ui.lineEdit.text()
    port = int(ui.lineEdit_3.text())
    user = ui.lineEdit_2.text()
    passwd = ui.lineEdit_4.text()
    try:
        s = ftp.connect(host = host,port = port)
        ui.callbacklog(ftp.welcome)
        ftp.login(user=user,passwd=passwd)
        # dir = cat_dir(ftp,filepath='/')
        ftp.cwd(remote_dir)
        ftp.status = True
        #ui.filedir(dir)
        loadremoteList(ftp,ui)
    except(socket.error, socket.gaierror):
        ui.showDialog()
        ui.callbacklog("failure connected")
        ftp.status = False
    except error_perm:
        ui.showDialog()
        ui.callbacklog("failure authentication")
        ftp.status = False
    
def loadremoteList(ftp,ui):
    templist = []
    ftp.dir()
    ftp.dir('.',templist.append)
    
    icon     = qIcon('folder.png')
    filename = ".."
    size = ""
    owner= ""
    group= ""
    date = ""
    mode = ""
    item = QTreeWidgetItem()
    item.setIcon(0,icon)
    for n, i in enumerate((filename, size, owner, group, date, mode)):
        item.setText(n, i)
    ui.fileList.addTopLevelItem(item)
    for content in templist:
        mode, num, owner, group, size, date, filename = parseFileInfo(content)
        if content.startswith('d'):
            icon     = qIcon('folder.png')
            pathname = os.path.join(ftp.pwd(), filename)
            remoteDir[pathname] = True
            remoteFilelist.append(filename)
        else:
            icon     = qIcon('file.png')
        item = QTreeWidgetItem()
        item.setIcon(0,icon)
        for n, i in enumerate((filename, size, owner, group, date, mode)):
            item.setText(n, i)
        ui.fileList.addTopLevelItem(item)
        if not ui.fileList.currentItem():
            ui.fileList.setCurrentItem(ui.fileList.topLevelItem(0))
            ui.fileList.setEnabled(True)

def parseFileInfo(file):
    item = [f for f in file.split(' ') if f != '']
    print(item)
    mode, num, owner, group, size, date, filename = (
    item[0], item[1], item[2], item[3], item[4], ' '.join(item[5:8]), ' '.join(item[8:])
    )
    return (mode, num, owner, group, size, date, filename)

def clearremoteList(ftp):
    remoteFilelist=[]

def openremotepath(ftp,ui):
    # 打开上一级目录
    if str(ui.fileList.currentItem().text(0)) == '..':
        if len(back_dir)<=1:
            return
        else: 
            back_dir.pop()
            remote_dir = back_dir[-1]
            ftp.cwd(remote_dir)
            clearremoteList(ftp)
            ui.fileList.clear()
            loadremoteList(ftp,ui)
    # # 打开下一级目录
    else:
        pathname = os.path.join(ftp.pwd(),str(ui.fileList.currentItem().text(0)))
        if is_ftp_dir(pathname):
            ftp.cwd(pathname)
            #back_dir = remote_dir
            remote_dir = ftp.pwd()
            back_dir.append(remote_dir)
            clearremoteList(ftp)
            ui.fileList.clear()
            loadremoteList(ftp,ui)
    




def closeftp(ftp):
    ftp.close()
    print("close success")

def is_ftp_file(ftp, ftp_path):
    try:
        if ftp_path in ftp.nlst(os.path.dirname(ftp_path)):
            return True
        else:
            return False
    except error_perm:
        return False
def is_ftp_dir(path):
    return remoteDir.get(path,None)

def uploadfile(ftp,remotepath,ui):
    fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件", os.getcwd(), 
        "All Files(*);;Text Files(*.txt)")
    print("----------------")
    print(fileName)
    bufsize = 1024
    fp = open(fileName, 'rb')
    print("----------------")
    res = ftp.storbinary('STOR ' + remote_dir+"/a.txt", fp, bufsize)  # 上传文件
    if res.find('226') != -1:
        ('upload file complete', remotepath)
    ftp.set_debuglevel(0)

def download(ftp,ui):
    filesize = int(ui.fileList.currentItem().text(1))
    # try:
    #     bufsize = 1024
    #     srcfile  = os.path.join(ftp.pwd(), str(ui.fileList.currentItem().text(0).toUtf8()))
    #     print("11111111111111")
    #     fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件", os.getcwd(), 
    #     "All Files(*);;Text Files(*.txt)")
    #     print("2222222222222")
    #     fp = open(filename,'wb')
    #     print("333333333333")
    #     res = ftp.retrbinary(
    #     'RETR ' + srcfile,
    #     fp.write,
    #     bufsize)
    #     if res.find("226") !=-1:
    #         print("download complete")
    #     f.close()
    # except AttributeError:
    #     print("failure!")
    bufsize = 1024
    srcfile  = ftp.pwd()+'/'+str(ui.fileList.currentItem().text(0))
    fileName = QtWidgets.QFileDialog.getExistingDirectory(None,"选取路径", os.getcwd())
    filename = fileName+ '/' + str(ui.fileList.currentItem().text(0))
    try:
        fp = open(filename,'wb+')
    except:
        pass
    res = ftp.retrbinary(
    'RETR ' + srcfile,
    fp.write,
    bufsize)
    if res.find("226") !=-1:
        print("download complete")
    f.close()
# 新建文件夹
def makedir(ftp,ui):
    if ftp.status == False:
        ui.showDialog()
        return
    filename = ui.NewNameDialog()
    ftp.mkd(remote_dir + filename)

# 重命名
def rename(ftp,ui):
    if ftp.status == False:
        ui.showDialog()
        return
    nowfilename = srcfile  = ftp.pwd()+'/'+str(ui.fileList.currentItem().text(0))
    filename = ui.NewNameDialog()
    ftp.rename(nowfilename , ftp.pwd()+'/' + filename )



# for test
def click_success():
    print("success")
def open_file():
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件", os.getcwd(), 
        "All Files(*);;Text Files(*.txt)")


# def showMenu(ui):
#     item = ui.fileList.currentItem()
#     #item1 = ui.fileList.itemAt(pos)
#     menu = QMenu()
#     download = menu.addAction(QAction(u'下载'))
#     # download.triggered.connect(self.testDownload)
#     property = menu.addAction(QAction(u"属性"))
#     # property.triggered.connect(self.testProperty)
#     menu.exec_(QCursor.pos())
#     print("sdsa")

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ftp_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    # 前端与后端相连接
    ui.pushButton.clicked.connect(partial(connect,ftp,ui))
    ui.pushButton_3.clicked.connect(partial(uploadfile,ftp,remote_dir,ui))
    ui.pushButton_4.clicked.connect(partial(closeftp,ftp))
    ui.pushButton_5.clicked.connect(partial(download,ftp,ui))
    ui.pushButton_2.clicked.connect(partial(makedir,ftp,ui))
    ui.pushButton_6.clicked.connect(partial(rename,ftp,ui))
    ui.fileList.itemDoubleClicked.connect(partial(openremotepath,ftp,ui))
    # ui.fileList.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
    # ui.fileList.customContextMenuRequested.connect(partial(showMenu,ui))  # 绑定事件

    MainWindow.show()    
    sys.exit(app.exec_())
    
