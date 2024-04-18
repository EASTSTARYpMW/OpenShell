import socket
import queue
import threading
import tkinter as tk
import sshui
import uuid

def thread_to_check(host,q,object):
    global success_info
    global fail_info
    while True:
        port = q.get()
        if port is None:
            q.task_done()
            break
        else:
            s = socket.socket()
            s.settimeout(1)
            try:
                s.connect((host,port))
                print(f'{port} 连接成功')
                success_info.append(f'{host}:{port}')

            except socket.error:
                print(f'{port} 端口连接失败')
                fail_info.append(f'{host}:{port}')

            q.task_done()
def create_threads(port1,port2,host='127.0.0.1',object1='',object2=''):
    global success_info
    global fail_info
    success_info = []
    fail_info = []
    num_threads = 5000
    port1 = int(port1)
    port2 = int(port2)
    q = queue.Queue()
    ports = range(port1+1,port2+1)
    object2.title('Scanning,Please wait')
    for port in ports:
        q.put(port)
    for i in range(num_threads):
        thread = threading.Thread(target=thread_to_check,args=(host,q,object))
        thread.start()
        # thread.join()
    q.join()
    print('扫描完成')
    print(success_info)
    print(fail_info)
    sshui.port_scan_textcontainer(success_info,fail_info,object1,object2)
