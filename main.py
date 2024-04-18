# OPENSSH, Version: 1.02

import paramiko
import threading
import time
import re
import json
from pathlib import Path
import keyboard
import multiprocess

import sshui


class ssh_connect():

    def __init__(self,url,port,user_name,password,connect_status,key_path):
        #主要变量
        self.port = port
        self.url = url
        self.user_name = user_name
        self.password = password
        self.connect_status = connect_status
        self.key_path = key_path
        #其他变量
        self.ssh = ''
        self.stdin = ''
        self.stdout = ''
        self.stderr = ''
        self.name = ''
        self.status = '200'
        self.channel = ''

        #    "流动变量"    initial instance
    def connect_server(self):
        if self.connect_status == 'none':
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.ssh.connect(hostname= self.url ,port=self.port ,username=self.user_name ,password=self.password,timeout=3)
            print('Connect Sucessfully')
            self.channel = self.ssh.invoke_shell()

        if self.connect_status == 'Key_connect':
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = paramiko.RSAKey(filename=self.key_path)
            self.ssh.connect(hostname=self.url, username=self.user_name, pkey=private_key,port=self.port,timeout=3)
            self.channel = self.ssh.invoke_shell()
            print('Connect Sucessfully')

    def ssh_interchange(self,input_command):
        self.stdin,self.stdout,self.stderr = self.ssh.exec_command(input_command)
        # stdin = self.stdin.read().decode('utf-8')
        # print(stdin)
        stdout = self.stdout.read().decode('utf-8')
        stderr = self.stderr.read().decode('utf-8')
        reply_list = [stdout,stderr]
        return reply_list

    def new_ssh_read(self):
        global last_output
        global input_status
        #Refresh screen
        if self.channel.recv_ready():
            output = self.channel.recv(2048*100)
            last_output = output
            output = output.decode('utf-8','replace')
            return [output, last_output]
        else:
            return ['none','none']

    def new_ssh_write(self,input_command):
        try:
            self.channel.send(input_command)
        except Exception as e:
            sshui.del_all()
            sshui.insert_text(e)
    def collect_name(self):
        a,name,c = self.ssh.exec_command('whoami')
        self.name = name.read().decode('utf-8')
        return self.name

    def download_files(self,remote_path,local_path):
        try:
            sftp = self.ssh.open_sftp()
            sftp.get(remote_path, local_path)
            print('Download successfully')
        except Exception as e:
            print(f'Download failed {e}')

    def upload_files(self,remote_path,local_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path,remote_path)
        print('Upload successfully')

    # def monitor_condition(self):
    #     connection_status = self.channel.active()
    #     return connection_status

def create_ssh(url,port,user_name,password,status,path):
    print(f'Connecting to {url}')
    new_server = ssh_connect(url=url,port=port,user_name=user_name,password=password,connect_status=status,key_path=path)
    new_server.connect_server()
    if new_server.status == '404':
        print('Terminal closing.')

    else:
        pass

    return new_server

def input_command(new_server):
    condition = 1
    while condition:
        name = new_server.collect_name()
        command = input(f'{name}:')
        if command[0] != '*':
            reply_lis = new_server.ssh_interchange(command)
            if reply_lis[0]:
                print(reply_lis[0])
            else:
                print(reply_lis[1])
        elif command[1:9] == 'download' :
            remote_path = input('RemotePath :')
            reply_path = new_server.ssh_interchange(f'ls {remote_path}')
            if reply_path[1]:
                print('Your path is out of remote path. ')
                continue
            local_path = input('Your local path :')
            if local_path is not True:
                local_path = '/'
            new_server.download_files(remote_path,local_path)
        elif command[1:7] == 'upload':
            # 留空，后面会更新其他功能
            # Will update
            pass
        else:
            new_server.ssh_close()
            print('---SSH CLOSED---')
            exit()

def new_input_command(new_server):
    condition = 1
    global ctrl_c_active
    global input_status
    global threading_status

    while condition:
        try:
            new_server.new_ssh_read()
        except EOFError:
            print('EOFERROR')
        input_command = input(':')
        if input_command:
            pass
        else:
            input_command = 'None'
        if input_command[0] != '*':
            if input_command[0] != '*':
            # print('ok')     #这里有问题
               new_server.new_ssh_write(input_command)
        elif input_command[1:9] == 'download':
            remote_path = input('RemotePath :')
            reply_path = new_server.ssh_interchange(f'ls {remote_path}')
            if reply_path[1]:
                print('Your path is out of remote path. ')
                input_status = 1
                continue
            local_path = input('Your local path :')
            if local_path is not True:
                local_path = '/'
            new_server.download_files(remote_path, local_path)
        elif input_command[1:7] == 'upload':
            print('Will update later')
            #Will update at version 1.02
        elif input_command[1:6] == 'close':
            print('-----SSH CLOSED-----')
            new_server.ssh.close()
            time.sleep(1)
            threading_status = 0
            del new_server
            exit()
        elif input_command[1:5] == 'help':
            print('*download for download\n*upload for upload\n*close for close ssh connection')
            input_status = 1
        else:
            print('Unknown command,please input ‘*help’ for help')
            input_status = 1
            continue

def json_read():
    try:
        all_info = []
        print('Checking json')
        path = Path('single_server_info.json')
        content = path.read_text()
        servers_info = json.loads(content)
        for server in servers_info:
            url = server['url']
            port = server['port']
            user_name = server['user_name']
            password = server['password']
            info = [url,port,user_name,password]
            all_info.append(info)
        return all_info
    except json.decoder.JSONDecodeError as e:
        print(f'json error {e}')
        time.sleep(1)
        exit()
    except KeyError as e:
        print(f'Key Error {e}')
        time.sleep(1)
        exit()

def init():
    global last_output
    global input_status
    global ctrl_c_active
    global tab_active
    global threading_status
    # global output
    threading_status = 0
    last_output = ''
    input_status = 0
    ctrl_c_active = 0
    tab_active = 0
    # output = ''

def use_vim():
    pass
    #will update at version 1.02

def check_event(new_server):
    global ctrl_c_active
    global input_status
    global tab_active
    global threading_status
    threading_status = 1
    while threading_status:
        try:
            if keyboard.is_pressed("ctrl+i"):
                # print('ctrl+c active!')  #for test
                ctrl_c_active = 1    #Nothing to use
                time.sleep(0.1)
                new_server.channel.send('\x03\n')
                input_status = 1
                # new_input_command()
                # new_server.new_ssh_read()
            if keyboard.is_pressed('tab'):
                tab_active = 1
        except KeyboardInterrupt:
            pass
            if threading_status == 0:
                break

def create_threading(new_server):
    print('Creating threads')
    thread = threading.Thread(target=check_event,args=(new_server,))
    thread.start()
    print('Create successfully')

if __name__ == '__main__':
    try:
        print('OPENSSH -version:1.01')
        print('Running')
        init()
        info = json_read()
        new_server = create_ssh(url=info[0],port=info[1],user_name=info[2],password=info[3])
    # 在json中替换你的服务器的端口信息 ，URL-------PORT----------USERNAME---------PASSWORD---------
    # replace the info from singe_server_info.json
        create_threading(new_server)
        new_input_command(new_server)
    except OSError as e:
        print(f'SSH ERROR {e}，this terminal will close at 2 second')
        # input_command(new_server)
        time.sleep(2)
        exit()