from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import configparser
import logging
import threading

#class FTP_server(threading.Thread):
class FTP_server(object):
    def __init__(self):
        super(FTP_server, self).__init__()
        self.ip = "127.0.0.1"
        self.port = '21'
        self.max_download = 100 * 1024
        self.max_upload = 100 * 1024
        self.max_cons = 100
        self.max_pre_ip = 10
        self.passive_port = (8300,8500)
        self.enable_anonymous = False
        self.anonymous_dir = ""
        self.log_file = r"..\pyftp.log"
        self.welcome_msg = "welcome!"
        self.server_status = False
    def setup(self):
        # 添加匿名用户 只需要路径
        self.dtp_handler = ThrottledDTPHandler
        self.authorizer = DummyAuthorizer()
        self.handler = FTPHandler
        if self.enable_anonymous == True:
            self.authorizer.add_anonymous(self.anonymous_dir)
        # 下载上传速度设置
        self.dtp_handler.read_limit = self.max_download
        self.dtp_handler.write_limit = self.max_upload
        # 添加被动端口范围
        self.handler.passive_ports = range(self.passive_port[0], self.passive_port[1])
        # 欢迎信息
        self.handler.banner = self.welcome_msg
        self.loadconfig()
        self.server = FTPServer((self.ip, self.port), self.handler)
        self.server.max_cons = self.max_cons
        self.server.max_cons_per_ip = self.max_pre_ip
    def loadconfig(self):
        config = configparser.ConfigParser()
        config.read("conf.ini")
        FTP = config.sections()[0]
        self.ip = config[FTP]["IP"]
        self.port = config[FTP]["PORT"]
        self.max_download = config[FTP]["MAX_DOWNLOAD"]
        self.max_upload = config[FTP]["MAX_UPLOAD"]
        self.max_cons = config[FTP]["MAX_CONS"]
        self.max_pre_ip = config[FTP]["MAX_PER_IP"]
        self.passive_port = list(config[FTP]["PASSIVE_PORT"])
        self.enable_anonymous = config[FTP]["ENABLE_ANONYMOUS"]
        self.anonymous_dir = config[FTP]["ANONYMOUS_DIR"]
        self.welcome_msg = config[FTP]["WELCOME_MSG"]
        users = configparser.ConfigParser()
        users.read('user.ini')
        user_list  = users.sections()
        for user in user_list:
            passwd = users[user]["password"]
            perm = users[user]["perm"]
            home_dir = users[user]["home"]
            self.authorizer.add_user(user,passwd, homedir= home_dir, perm=perm)
        self.handler.authorizer = self.authorizer
    def startServer(self):
        self.server_status = True
        self.server.serve_forever()
    def close(self):
        self.server_status = False
        self.server.close_all()

if __name__ == "__main__":
    ftpserver = FTP_server()
    ftpserver.startServer()