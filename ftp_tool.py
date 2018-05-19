from ftplib import FTP
import os
import sys
# import string
# import datetime
import time
import socket
import argparse


class FTP_Tool(object):
    def __init__(self, host_addr, username, password, remote_dir, port=21):
        self.host_addr = host_addr
        self.username = username
        self.password = password
        self.remote_dir = remote_dir
        self.port = port
        self.ftp = FTP()
        self.file_list = []

        # self.ftp.set_debuglevel(2)
    def __del__(self):
        self.ftp.close()

    def login(self):
        ftp = self.ftp

        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print("Starting to conncet to {}".format(self.host_addr))
            ftp.connect(self.host_addr, self.port)
            print("Successfully connect to ftp server!")
            print("Starting to log in with: {}".format(self.username))
            ftp.login(self.username, self.password)
            print("Successfully log in with {}".format(self.username))
            debug_print(ftp.getwelcome())
        except Exception as e:
            print("Conncet/Login error")
            deal_error(e)

        try:
            ftp.cwd(self.remote_dir)
        except Exception as e:
            print("Change folder error")
            deal_error(e)

    def is_same_size(self, local_file, remote_file):
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception:
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception:
            local_file_size = -1

        debug_print("lo:{} re:{}".format(local_file_size, remote_file_size))


        if remote_file_size == local_file_size:
            return 1
        else:
            return 0

    def download_file(self, local_file, remote_file):
        if self.is_same_size(local_file, remote_file):
            debug_print("With same size, no need to download:{}".format(remote_file))

        else:
            debug_print(">>>>>>>>>>>>>>>Downloading file:{}".format(remote_file))

        file_handler = open(local_file, "wb")
        self.ftp.retrbinary('RETR %s'%(remote_file), file_handler.write)

        file_handler.close()

    def download_files(self, local_dir ='./', remote_dir='./'):
        try:
            self.ftp.cwd(remote_dir)
        except:
            debug_print('Folder not exist! Folder:{}'.format(remote_dir))

        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)

        debug_print('Change folder to {}'.format(self.ftp.pwd()))
        self.file_list = []
        self.ftp.dir(self.file_list.append)
        remote_names = self.file_list

        for item in remote_names:
            file_type = item[0]
            file_name = item[(item.rfind(':')+4):]

            local = os.path.join(local_dir, file_name)
            if file_type == 'd':
                if file_name not in ['.', '..']:
                    self.download_files(local, file_name)
            elif file_type == '-':
                self.download_file(local, file_name)
        self.ftp.cwd('..')
        debug_print('Return to parent directory:{}'.format(self.ftp.pwd()))

    def upload_files(self, local_dir = './', remote_dir = './'):
        if not os.path.isdir(local_dir):
            return

        local_names = os.listdir(local_dir)
        self.ftp.cwd(remote_dir)
        for item in local_names:
            src = os.path.join(local_dir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print('Folder:{} exists in FTP server'.format(item))
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)

        self.ftp.cwd('..')
        # import pdb; pdb.set_trace()

    def upload_file(self, local_file, remote_file):
        if not os.path.isfile(local_file):
            return
        # if self.is_same_size

        file_handler = open(local_file, 'rb')
        #try:
        #    self.ftp.delete(remote_file)
        #except Exception as e:
        #    pass
        # import pdb;pdb.set_trace()
        # self.ftp.storbinary('STOR {}'.format(remote_file), file_handler)
        self.ftp.storbinary('STOR {}'.format(local_file), file_handler)
        # self.ftp.delete(remote_file)
        # self.ftp.storbinary('STOR {}'.format(remote_file), file_handler)

        file_handler.close()
        debug_print('Update {} finished.'.format(local_file))

def debug_print(message):
    print(message)

def deal_error(e):
    time_now = time.localtime()
    date_now = time.strftime("%Y-%m-%d", time_now)
    logstr = "{}.Error occurred!:{}".format(date_now, e)
    debug_print(logstr)
    file.write(logstr)
    sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(description='FTP Toolbox')
    parser.add_argument('--host-addr', help='FTP host address', required=True, type=str)
    parser.add_argument('--username', help='FTP Server username', required=True, type=str)
    parser.add_argument('--password', help='FTP Server password',
    required=True, type=str)
    parser.add_argument('--local-dir', help='Local file/files to be uploaded', required=True, type=str)
    parser.add_argument('--remote-dir', help='FTP remote folder name',required=True, type=str)
    parser.add_argument('--time', help='Sleep time for update files to ftp server', required=True, type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    file = open("./log.txt", "a")

    time_now = time.localtime()
    date_now = time.strftime('%Y-%m-%d', time_now)
    logstr = date_now

    args = parse_args()

    # config
    host_addr = args.host_addr
    username = args.username
    password = args.password
    port = 21
    # rootdir_local
    root_dir_remote = args.remote_dir

    f = FTP_Tool(host_addr, username, password, root_dir_remote, port)
    f.login()
    # f.download_files("./backup", './')
    # f.upload_files(args.local_dir, './')
    import time
    from update_stat import build_gpu_html

    while True:
        print(time.strftime("%Y-%m-%d %H:%M"),)
        build_gpu_html()
        f.upload_file('./p40gpu.html', './')
        time.sleep(args.time)
