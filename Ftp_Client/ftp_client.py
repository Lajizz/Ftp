import socket
import os,sys
import ftplib
from ftplib import FTP
import ftp_ui
from ftp_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from ftplib import error_perm


def connect(ftp,ui):
    host = ui.lineEdit.text()
    port = int(ui.lineEdit_3.text())
    user = ui.lineEdit_2.text()
    passwd = ui.lineEdit_4.text()
    try:
        ftp.close()
        ui.clear()
        ui.fileList.clear()
    except:
        pass

    try:
        s = ftp.connect(host = host,port = port)
        ui.callbacklog("status:success connected")
        ftp.login(user=user,passwd=passwd)
        # dir = cat_dir(ftp,filepath='/')
        ftp.cwd(remote_dir)
        ftp.status = True
        #ui.filedir(dir)
        loadremoteList(ftp,ui)
    except(socket.error, socket.gaierror):
        ui.showDialog("")
        ui.callbacklog("status: failure connected")
        ftp.status = False
    except error_perm:
        ui.showDialog("")
        ui.callbacklog("status: failure authentication")
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
            # back_dir = remote_dir
            remote_dir = ftp.pwd()
            back_dir.append(remote_dir)
            clearremoteList(ftp)
            ui.fileList.clear()
            loadremoteList(ftp,ui)

def closeftp(ftp,ui):
    ftp.close()
    ui.clear()
    ui.fileList.clear()
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
    try:
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None,"选取文件", os.getcwd(), 
            "All Files(*);;Text Files(*.txt)")
        name = fileName.split('/')[-1]  #得到文件名字
        bufsize = 1024
        fp = open(fileName, 'rb')

        res = ftp.storbinary('STOR '+ back_dir[-1]+"/"+name, fp, bufsize)  # 上传文件
        if res.find('226') != -1:
            ('upload file complete', remotepath)
            ui.showDialog("status: upload success")
            ui.callbacklog("status: upload success")
        ftp.set_debuglevel(0)
    except:
        ui.showDialog("status: upload permission Deny")
        ui.callbacklog("status: upload permission Deny")


def download(ftp,ui):
    
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
    try:
        filesize = int(ui.fileList.currentItem().text(1))
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
            ui.showDialog("status: download success")
            ui.callbacklog("status: download success")
        fp.close()
    except AttributeError:
        ui.showDialog("status: download permission Deny")
        ui.callbacklog("status: download permission Deny")

# 新建文件夹
def makedir(ftp,ui):
    if ftp.status == False:
        ui.showDialog()
        return
    try:
        filename = ui.NewNameDialog()
        ftp.mkd(remote_dir + filename)
    except:
        ui.showDialog("status: make dir permission Deny")
        ui.callbacklog("status: make dir permission Deny")
def ok(ui):
    print("ok")
def cancel(ui):
    ui.cancel()
# 重命名
def rename(ftp,ui):
    try:
        nowfilename = srcfile  = ftp.pwd()+'/'+str(ui.fileList.currentItem().text(0))
        filename = ui.NewNameDialog()
        ftp.rename(nowfilename , ftp.pwd()+'/' + filename )
    except:
        ui.showDialog("status: rename operation failure")
        ui.callbacklog("status: rename operation failure")



def rightdown():
    download(ftp,ui)
def rightrename():
    rename(ftp,ui)
def rightmkdir():
    mkdir(ftp,ui)

def showMenu(ftp,ui):
    
    #item = ui.fileList.currentItem()
    #item1 = ui.fileList.itemAt(pos)
    icon     = qIcon('download.jpg')
    menu = QMenu()
    down = QAction(icon,u'下载')
    menu.addAction(down)
    down.triggered.connect(rightdown)

    icon     = qIcon('rename.jpg')
    re = QAction(icon,u"重命名")
    menu.addAction(re)
    re.triggered.connect(rightrename)

    icon     = qIcon('folder.png')
    mk = QAction(icon,u'新建文件夹')
    menu.addAction(mk)
    mk.triggered.connect(rightmkdir)

    menu.setWindowModality(QtCore.Qt.ApplicationModal)
    # property.triggered.connect(self.testProperty)
    menu.exec_(QCursor.pos())


def makeconnect(ui):
    ui.pushButton.clicked.connect(partial(connect,ftp,ui))
    ui.pushButton_3.clicked.connect(partial(uploadfile,ftp,remote_dir,ui))
    ui.pushButton_4.clicked.connect(partial(closeftp,ftp,ui))
    ui.pushButton_5.clicked.connect(partial(download,ftp,ui))
    ui.pushButton_2.clicked.connect(partial(makedir,ftp,ui))
    ui.pushButton_6.clicked.connect(partial(rename,ftp,ui))
    ui.fileList.itemDoubleClicked.connect(partial(openremotepath,ftp,ui))
    ui.fileList.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
    ui.fileList.customContextMenuRequested.connect(partial(showMenu,ui))  # 绑定事件
    ui.okBtn.clicked.connect(partial(ok,ui))
    ui.cancelBtn.clicked.connect(partial(cancel,ui))



if  __name__ == "__main__":
    app_icon_path = os.path.join(os.path.dirname(__file__), 'icon')
    qIcon = lambda name: QtGui.QIcon(os.path.join(app_icon_path, name))
    ftp = FTP()
    ftp.status = False
    ftp.set_debuglevel(0)
    back_dir = ['/']
    remote_dir = '/'
    remoteFilelist = []
    remoteDir = {}
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    makeconnect(ui)
    MainWindow.show()    
    sys.exit(app.exec_())
    
