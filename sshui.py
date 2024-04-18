# OPENSSH -UI  version:1.10
#作者：EASTSTAR_YpMW
#邮箱：Hoplnd6@gmail.com
import ddos_attack
import main
import tkinter as tk
import os
import time
import json
import threading
import re
from tkinter import filedialog
import stream_client
import webbrowser
import check_port
import web_static_server

Welecome_text = 'Welecome to use OpenShell -UI Version 1.10'

def set_proxy(status,host='',port=''):
    
    if status == 'proxy_connect':
        print(host,port)
        os.environ['HTTP_PROXY'] = f'{host}:{port}'
        os.environ['HTTPS_PROXY'] = f'{host}:{port}'
    if status == 'default':
        os.environ['HTTP_PROXY'] = ''
        os.environ['HTTPS_PROXY'] = ''
    else:
        pass

def create_root():
    global text_container
    global root
    root = tk.Tk()
    root.title("OpenShell -1.10")
    root.geometry("1080x720")
    # root.iconbitmap(r"openshell.ico")
    root.resizable(False,False)
    #放置容器，其用来填充url等信息
    container_read = tk.Frame(master=root,bg='blue',width=1080,height=30)
    container_show = tk.Frame(master=root,bg='blue',width=1080,height=80)
    container_show.pack(anchor = 'ne', side = 'top')
    container_read.pack(anchor = 'nw', side = 'top')
    text_container = tk.Text(container_read,wrap=tk.WORD,bg="#333333",fg=check_settings(),width=1080,height=35,font=('Consolas', 11))
    text_container.insert(tk.END,Welecome_text)
    text_container.config(state='disabled')
    text_container.pack(side = 'top',anchor = 'nw')
    input_container = tk.Frame(master=root,bg='red',width=1080,height=20)
    input_container.pack()
    function_container = tk.Frame(master=root,width=1080,height=30)
    function_container.pack()
    create_Entery(root, container_show, input_container, text_container,function_container)
    return [root,container_read,container_show,text_container,input_container,function_container]

#放置button，Entry
def create_Entery(root,container_show,input_container,text_container,function_container):
    lab_url = tk.Label(container_show,text='URL:')
    ent_url = tk.Entry(master=container_show,width=25)
    lab_password = tk.Label(container_show, text='PASSWORD:')
    ent_password = tk.Entry(master=container_show,width=25,show='#')
    lab_username = tk.Label(container_show,text='USERNAME:')
    ent_username = tk.Entry(master=container_show,width=25)
    lab_port = tk.Label(master=container_show,width=5,text='PORT:')
    ent_port = tk.Entry(master=container_show,width=10)
    ent_port.insert(tk.END,22)
    button_check = tk.Button(master=container_show,width=10,text='CONNECT',command=lambda :connect(ent_url.get(),ent_username.get(),ent_password.get(),port=ent_port.get()))
    button_unconnect = tk.Button(master=container_show,width=10,text='UNCONNECT',command=lambda :del_all())
    button_key_login = tk.Button(master=container_show,width=12,text='KEY LOGIN',command=lambda :create_levelroot('key_login',root))
    for all_things in ([lab_url,ent_url,lab_username,ent_username,lab_password,ent_password,lab_port,ent_port,button_check,button_unconnect,button_key_login]):
        all_things.pack(side = 'left')
    ent_command = tk.Entry(master=input_container,width=120)
    ent_command.pack(side = 'left')
    #检测按键活动
    root.bind('<Return>', lambda event: check_event('enter',ent_command,'none'))
    root.bind('<Tab>',lambda event: check_event('tab',ent_command,'none'))
    root.bind('<Control-c>', lambda event: check_event('ctrl-c','none','none'))
    root.bind('<Up>',lambda event: check_event('up','none',ent_command))
    root.bind('<Down>',lambda event: check_event('down','none',ent_command))
    root.bind('<Escape>',lambda event: check_event('esc','none','none'))
    root.bind('<Button-3>',lambda event: create_menu(object01=root))
    #放置ENTER,CLEAR
    Button_in = tk.Button(master=input_container,width=20,text='ENTER',command=lambda : check_event('enter',ent_command,'none'))
    Button_clear = tk.Button(master=input_container,width=20,text='CLEAR',command=lambda :clear_container(text_container))
    Button_down = tk.Button(master=function_container,text='DOWNLOAD',width=20,command=lambda :create_levelroot('download',root))
    Button_up = tk.Button(master=function_container,text='UPLOAD',width=20,command=lambda :create_levelroot('upload',root))
    Button_checkjson = tk.Button(master=function_container,text='CHECK JSON',width=20,command=lambda :create_levelroot('check_json',root))
    Button_help = tk.Button(master=function_container,text='EDIT',width=20,command=lambda :create_levelroot('edit',root))
    Button_proxy = tk.Button(master=function_container,text='SCAN PORT',width=20,command=lambda :create_levelroot('port',root))
    Button_stream = tk.Button(master=function_container,text='STATIC WEB',width=20,command=lambda :create_levelroot('establish_web',root))
    lab_coms = tk.Button(master=function_container,text='SETTINGS',width=27,command=lambda :create_levelroot('settings',root))
    for button in (Button_in,Button_clear,Button_down,Button_up,Button_help,Button_checkjson,Button_proxy,Button_stream,lab_coms):
        button.pack(side='left')

def create_levelroot(status, object):
    global text_container
    if status == 'key_login':
        key_login_level = tk.Toplevel(object)
        key_login_level.geometry('300x120')
        key_login_level.resizable(False, False)
        key_login_level.title('Key Login')
        container_url = tk.Frame(master=key_login_level, bg='blue', width=300, height=80)
        container_name = tk.Frame(master=key_login_level, bg='red', width=300, height=80)
        container_port = tk.Frame(master=key_login_level,bg='blue',width=300,height=80)
        container_key = tk.Frame(master=key_login_level, bg='blue', width=300, height=80)
        # container_connect = tk.Frame(master=key_login_level,bg='yellow',width=300,height=80)
        for container in (container_url,container_name,container_port,container_key):
            container.pack()
        lab_url = tk.Label(master=container_url,text='URL:',width=10)
        ent_url = tk.Entry(master=container_url, width=30)
        lab_name = tk.Label(master=container_name,text='USERNAME:',width=10)
        ent_name = tk.Entry(master=container_name,width=30)
        lab_port = tk.Label(master=container_port,width=10,text='PORT:')
        ent_port = tk.Entry(master=container_port,width=30)
        ent_port.insert(tk.END,22)
        lab_key = tk.Label(master=container_key,text='KEY:',width=10)
        but_key = tk.Button(master=container_key,width=30,text='OPEN FILE DIALOG',command=lambda :open_file_dialog(ent_url,ent_name,ent_port))
        for all_things in (lab_url,ent_url,lab_name,ent_name,lab_port,ent_port,lab_key,but_key):
            all_things.pack(side = 'left')

    if status == 'download':
        # elseui.create_download_root(object=object)
        download_level = tk.Toplevel(object)
        download_level.geometry('300x150')
        download_level.title('Download')
        download_level.resizable(False, False)
        container_re = tk.Frame(master=download_level, bg='blue', width=300, height=80)
        container_lo = tk.Frame(master=download_level, bg='red', width=300, height=80)
        container_do = tk.Frame(master=download_level, bg='blue', width=300, height=80)
        for container in (container_re, container_lo, container_do):
            container.pack()
        lab_remote = tk.Label(master=container_re, text='REMOTE PATH:',width=13)
        ent_remote = tk.Entry(master=container_re, width=30)
        lab_local = tk.Label(master=container_lo, text='LOCAL PATH:',width=13)
        ent_local = tk.Entry(master=container_lo, width=30)
        but_download = tk.Button(master=container_do, width=30, text='DOWNLOAD',command=lambda: sftp('download', ent_remote, ent_local))
        for things in (lab_remote, ent_remote, lab_local, ent_local, but_download):
            things.pack(side='left')

    if status == 'upload':
        upload_level = tk.Toplevel(object)
        upload_level.geometry('300x150')
        upload_level.resizable(False, False)
        upload_level.title('Upload')
        container_re = tk.Frame(master=upload_level, bg='blue', width=300, height=80)
        container_lo = tk.Frame(master=upload_level, bg='red', width=300, height=80)
        container_do = tk.Frame(master=upload_level, bg='blue', width=300, height=80)
        for container in (container_re, container_lo, container_do):
            container.pack()
        lab_remote = tk.Label(master=container_re, text='REMOTE PATH:',width=13)
        ent_remote = tk.Entry(master=container_re, width=30)
        lab_local = tk.Label(master=container_lo, text='LOCAL PATH:',width=13)
        ent_local = tk.Entry(master=container_lo, width=30)
        but_download = tk.Button(master=container_do, width=30, text='UPLOAD',command=lambda: sftp('upload', ent_remote, ent_local))
        for things in (lab_remote, ent_remote, lab_local, ent_local, but_download):
            things.pack(side='left')

    if status == 'check_json':
        json_level = tk.Toplevel(object)
        json_level.geometry('300x300')
        json_level.resizable(False, False)
        json_level.title('Check json')
        container_check = tk.Frame(master=json_level,width=300,height=30,background='blue')
        container_show = tk.Frame(master=json_level,width=300,height=300,background='red')
        for container in (container_check,container_show):
            container.pack()
        but_check = tk.Button(master=container_check,text='CHECK',width=100,command= lambda :check_json(object01=json_level,object02=container_show))
        for thing in (but_check,):
            thing.pack(side = 'left')

    if status == 'edit':
        edit_level = tk.Toplevel(object)
        edit_level.geometry('350x150')
        edit_level.resizable(False, False)
        edit_level.title('Edit files')
        container_remote_path = tk.Frame(master=edit_level,width=350,height=80,background='blue')
        container_but = tk.Frame(master=edit_level,width=300,height=80,background='red')
        container_vscode = tk.Frame(master=edit_level,width=300,height=80,background='blue')
        for thing in (container_remote_path,container_but,container_vscode):
            thing.pack()
        lab_re = tk.Label(master=container_remote_path,text='REMOTE PATH:',width=13)
        ent_remote = tk.Entry(master=container_remote_path,width=300)
        but_open = tk.Button(master=container_but,width=30,text='OPEN FILE WITH NOTEBOOK',command= lambda :edit_files(status='open',path=ent_remote.get()))
        but_active = tk.Button(master=container_but,width=20,text='ACTIVE',command= lambda :edit_files(status='active',path=ent_remote.get()))
        but_vscode = tk.Button(master=container_vscode,width=50,text='OPEN WITH VSCODE',command=lambda :edit_files(status='vscode',path=ent_remote.get()))
        for thing in (lab_re,ent_remote,but_open,but_active,but_vscode):
            thing.pack(side = 'left')

    if status == 'port':
        port_level = tk.Toplevel(object)
        port_level.geometry('300x150')
        port_level.resizable(False, False)
        port_level.title('Scan port')
        host_container = tk.Frame(master=port_level,width=300,height=80,bg='red')
        port_container = tk.Frame(master=port_level,width=300,height=80,bg='blue')
        but_container = tk.Frame(master=port_level,width=300,height=80,bg='red')
        for thing in (host_container,port_container,but_container):
            thing.pack()
        lab_host = tk.Label(master=host_container,width=10,text='HOST:')
        ent_host = tk.Entry(master=host_container,width=30)
        lab_port1 = tk.Label(master=port_container,width=10,text='PORT:')
        ent_port1 = tk.Entry(master=port_container,width=10)
        lab_port2 = tk.Label(master=port_container,width=9,text='TO')
        ent_port2 = tk.Entry(master=port_container,width=10)
        but_check = tk.Button(master=but_container,width=20,text='SCAN',bg='red',command=lambda :check_port.create_threads(host=ent_host.get(),port1=ent_port1.get(),port2=ent_port2.get(),object1=text_container,object2=port_level))
        for object in (lab_host,ent_host,lab_port1,ent_port1,lab_port2,ent_port2,but_check):
            object.pack(side = 'left')

    if status == 'stream':
        settings_level = tk.Toplevel(object)
        settings_level.geometry('300x150')
        settings_level.resizable(False, False)
        settings_level.title('Stream**Beta')
        container_host = tk.Frame(master=settings_level,width=300,height=80,background='blue')
        container_port = tk.Frame(master=settings_level,width=300,height=80,background='red')
        container_button = tk.Frame(master=settings_level,width=300,height=80,background='blue')
        container_default = tk.Frame(master=settings_level,width=300,height=80,background='red')
        for container in (container_host,container_port,container_button,container_default):
            container.pack()
        label_host = tk.Label(master=container_host,width=15,text='SERVER HOST:')
        entry_host = tk.Entry(master=container_host,width=30)
        label_port = tk.Label(master=container_port,width=15,text='PORT:')
        entry_port = tk.Entry(master=container_port,width=30)
        but_host = tk.Button(master=container_button,width=15,text='I AM HOST',command=lambda :stream(status='host',host=entry_host.get(),port=entry_port.get()))
        but_visitor = tk.Button(master=container_button,width=15,text='I AM VISITOR',command=lambda :stream(status='visitor',host=entry_host.get(),port=entry_port.get()))
        but_default = tk.Button(master=container_default,width=30,text='DEFAULT',command=del_host)
        for show_thing in (label_host,entry_host,label_port,entry_port,but_host,but_visitor,but_default):
            show_thing.pack(side = 'left')

    if status == 'establish_web':
        web_level = tk.Toplevel(object)
        web_level.geometry('300x150')
        web_level.resizable(False, False)
        web_level.title('Static web**Beta')
        container_path = tk.Frame(master=web_level,width=300,height=80,background='yellow')
        container_port = tk.Frame(master=web_level,width=300,height=80,background='red')
        container_button = tk.Frame(master=web_level,width=300,height=80,background='blue')
        container_cz = tk.Frame(master=web_level,width=300,height=80)
        for object in (container_path,container_port,container_button,container_cz):
            object.pack()
        label_path = tk.Label(master=container_path,width=15,text='PATH:')
        ent_path = tk.Entry(master=container_path,width=30)
        ent_path.insert(tk.END,'./')
        label_port = tk.Label(master=container_port,width=15,text='PORT:')
        entry_port = tk.Entry(master=container_port,width=30)
        entry_port.insert(tk.END,'8848')
        but_establish = tk.Button(master=container_button,width=15,text='RUN.',command=lambda :web_static_server._thread(status='active',PORT=entry_port.get(),object=text_container,web_root=ent_path.get()))
        but_cancel = tk.Button(master=container_button,width=15,text='CANCEL.',command=lambda :web_static_server._thread(status='cancel',object=text_container))
        lab_cz = tk.Label(master=container_cz,width=30,text='***Supported by CrazySand***')
        for object in (label_path,ent_path,label_port,entry_port,but_establish,but_cancel,lab_cz):
            object.pack(side = 'left')

    if status == 'settings':
        _settings_level = tk.Toplevel(object)
        _settings_level.geometry('300x150')
        _settings_level.resizable(False, False)
        _settings_level.title('Settings')
        web_container = tk.Frame(master=_settings_level,width=300,height=80)
        setting_container = tk.Frame(master=_settings_level,width=300,height=80,bg='blue')
        maker_container = tk.Frame(master=_settings_level,width=300,height=80,bg='yellow')
        ddos_container = tk.Frame(master=_settings_level,width=300,height=40,bg='yellow')
        for thing in (web_container,setting_container,ddos_container,maker_container):
            thing.pack()
        vis_lab = tk.Label(master=web_container,width=30,text='VISIT OUR WEBSITE--->')
        vis_but = tk.Button(master=web_container,width=15,text='eaststar.ltd',command=lambda: webbrowser.open('eaststar.ltd'),bg='grey')
        change_lab = tk.Label(master=setting_container,width=22,text='Change your text color--->')
        but_red = tk.Button(master=setting_container,bg='red',width=5,command=lambda :change_color('red'))
        but_green = tk.Button(master=setting_container,bg='green',width=5,command=lambda :change_color('green'))
        but_white = tk.Button(master=setting_container,bg='white',width=5,text='white',command=lambda :change_color('white'))
        lab_maker = tk.Label(master=maker_container,text='---Designed by EASTSTAR_YpMW---')
        lab_ddos = tk.Label(master=ddos_container,text="ddos attack ",width=22)
        but_ddos = tk.Button(master=ddos_container,text='Attack',width=15,command= lambda :ddos_attack.ddos_level(object,text_container))
        for _thing in (vis_lab,vis_but,change_lab,but_red,but_green,but_white,lab_maker,lab_ddos,but_ddos):
            _thing.pack(side = 'left')

def port_scan_textcontainer(success,fail,text_container,port_level):
    port_level.title('Scan Port')

    # text_container.config(state='normal')
    # text_container.insert(tk.END, f"\n------------FAILURE------------\n")
    # text_container.config(state='disabled')
    #
    # for fail_info in fail:
    #     text_container.config(state='normal')
    #     text_container.insert(tk.END,f"---{fail_info} status:Inactive\n")
    #     text_container.config(state='disabled')
    #     text_container.see(tk.END)

    text_container.config(state='normal')
    text_container.insert(tk.END, f"\n------------SUCCESS------------\n")
    text_container.config(state='disabled')
    text_container.see(tk.END)

    for info in success:
        text_container.config(state='normal')
        text_container.insert(tk.END,f"---{info}  status:Active\n")
        text_container.config(state='disabled')
        text_container.see(tk.END)

def change_color(choose_color):
    global text_container
    if choose_color == 'red':
        text_container.config(fg='red')
        data = {'color':'red'}
        with open('settings.json', 'w') as json_file:
            json.dump(data, json_file)

    if choose_color == 'green':
        text_container.config(fg='green')
        data = {'color':'green'}
        with open('settings.json', 'w') as json_file:
            json.dump(data, json_file)

    if choose_color == 'white':
        text_container.config(fg='white')
        data = {'color':'white'}
        with open('settings.json', 'w') as json_file:
            json.dump(data, json_file)

def check_settings():
    if not os.path.exists('settings.json'):
        _data = {'color':'red'}
        with open('settings.json', 'w') as json_file:
            json.dump(_data, json_file)
        print("初始化完成")
        return 'red'
    else:
        with open('settings.json', "r") as json_file:
            data = json.load(json_file)
            color = data['color']
            return color

def stream(status,host,port):
    global stream_host
    global stream_vis
    if status == 'host':
        try:
            stream_client.establish_hostman(server_url=host, port=port)
            stream_host = 1
        except Exception as e:
            print(e)
    if status == 'visitor':
        try:
            stream_client.establish_visitor(server_url=host,port=port)
            stream_vis = 1
            create_threads(status='stream')
        except Exception as e:
            print(e)

def create_menu(status='',object01='',object02=''):
    menu = tk.Menu(master=object01,tearoff=False)
    menu.add_command(label='Copy',command=copy_callback)

def copy_callback():
    global text_container
    text_container.event_generate('<<Copy>>')

def edit_files(status='',path=''):
    if status == 'open':
        match = re.search(r'[^\/]+$', path)
        if match:
            file_name = match.group()
            print(f"File Name: {file_name}")
            os.makedirs("Cache_files", exist_ok=True)
            new_server.download_files(path, f"Cache_files/{file_name}")
            os.system(f"notepad.exe Cache_files/{file_name}")
        else:
            print("No match found.")

    if status == 'vscode':
        match = re.search(r'[^\/]+$', path)
        if match:
            file_name = match.group()
            print(f"File Name: {file_name}")
            os.makedirs("Cache_files", exist_ok=True)
            new_server.download_files(path, f"Cache_files/{file_name}")
            os.system(f"code Cache_files/{file_name}")

    if status == 'active':
        match = re.search(r'[^\/]+$', path)
        if match:
            file_name = match.group()
            print(f"File Name: {file_name}")
            new_server.upload_files(path,f"Cache_files/{file_name}")
        else:
            print("No match found.")

def check_json(object01='',object02=''):
    all_info = main.json_read()
    but_server01 = tk.Button(master=object02,text=f'{all_info[0][0]}    {all_info[0][2]}',command=lambda :connect(ent_url=all_info[0][0],ent_user_name=all_info[0][2],ent_password=all_info[0][3]),width=300)
    but_server01.pack()
    but_server02 = tk.Button(master=object02, text=f'{all_info[1][0]}    {all_info[1][2]}',command=lambda: connect(ent_url=all_info[1][0], ent_user_name=all_info[1][2],ent_password=all_info[1][3]), width=300)
    but_server02.pack(side = 'bottom')
    but_server03 = tk.Button(master=object02,text=f'{all_info[2][0]}    {all_info[2][2]}',command=lambda :connect(ent_url=all_info[2][0],ent_user_name=all_info[2][2],ent_password=all_info[2][3]),width=300)
    but_server03.pack(side = 'bottom')
    but_server04 = tk.Button(master=object02, text=f'{all_info[3][0]}    {all_info[3][2]}',command=lambda: connect(ent_url=all_info[3][0], ent_user_name=all_info[3][2],ent_password=all_info[3][3]), width=300)
    but_server04.pack(side = 'bottom')
def open_file_dialog(ent_url,ent_name,ent_port):
    file_path = filedialog.askopenfile(initialdir="/", title="Select file",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    connect(ent_url=ent_url,ent_user_name=ent_name,status='Key_connect',path=file_path,port=ent_port.get())

def connect(ent_url,ent_user_name,ent_password='none',path='none',status='none',port=22):
    try:
        global new_server
        global condition
        global text_container
        global root
        if new_server == 0:
            if status == 'none':

                if ent_url == '' or ent_user_name== '' or ent_password == '':
                    container_reads(text_container=text_container,status='empty url')
                    #抛出异常
                    error_num = 1/0
                    print(error_num)
                else:
                    new_server = main.create_ssh(url=ent_url,password=ent_password,port=port,user_name=ent_user_name,status=status,path=path)
                    container_reads(text_container,None)
                    print(new_server)

            if status == 'Key_connect':
                print('OK')
                url = ent_url.get()
                user_name = ent_user_name.get()
                new_server = main.create_ssh(url=url,user_name=user_name,path=path,port=port,status='Key_connect',password=ent_password)
                container_reads(text_container, None)

            root.title('Connection Active')

        else:
            container_reads(text_container=text_container,status='Connected',info="Connection has been created")

    except Exception as e:
        print(e)
        container_reads(text_container=text_container,status = '404',info=e)

def container_reads(text_container,status,info=''):
    # global new_server
    if status == '404':
        text_container.config(state='normal')
        text_container.insert(tk.END,f"\nCONNECTION WAS FAILED {info}")
        text_container.config(state='disabled')
        text_container.see(tk.END)

    if status == 'Connected':
        text_container.config(state='normal')
        text_container.insert(tk.END,f"\n{info}")
        text_container.config(state='disabled')
    if status == 'empty url':
        text_container.config(state='normal')
        text_container.insert(tk.END,f"\nSomething such as url,username,password is empty")
        text_container.config(state='disabled')

    if status == 'scan ok':
        text_container.config(state='normal')
        text_container.insert(tk.END,f"{info[0]}:{info[1]} yes.")
        text_container.config(state='disabled')

    if status == 'scan no':
        text_container.config(state='normal')
        text_container.insert(tk.END,f"{info[0]}:{info[1]} no.")
        text_container.config(state='disabled')

    else:
        create_threads()

def info_update(text_container):
    global thread
    global thread_condition
    global condition
    global stream_host
    global stream_vis
    condition = 1
    while thread_condition:
        while condition:
            # if not new_server.monitor_condition():
            #     thread_condition = 0
            time.sleep(0.01)
            reply = new_server.new_ssh_read()
            output = reply[0]
            last_output = reply[1]
            if output != 'none':
                cleaned_output = _remove_ansi_sequences(output)
                text_container.config(state='normal')
                text_container.insert(tk.END, f'\n{cleaned_output}')
                text_container.config(state='disabled')
                text_container.see(tk.END)
                print(cleaned_output.encode('utf-8'))
            elif stream_host == 1:
                stream_client.host_send(cleaned_output)
                print("send to server successfully")

            elif thread_condition == 0:
                break
            else:
                pass
        if thread_condition == 0:
            break

def _remove_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    text_without_x07 = re.sub(r'\x07', '', text)
    cleaned_text = ansi_escape.sub('', text_without_x07)
    return cleaned_text
    # ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    # return ansi_escape.sub('', text)

def clear_container(text_container):
    text_container.config(state='normal')
    text_container.delete("1.0", tk.END)
    text_container.config(state='disabled')

def container_write(ent_command):
    global new_server
    global text_container
    global condition
    condition = 1
    command = ent_command.get()
    new_server.new_ssh_write(command + '\n')
    history('write',command,'none')

#ctrl + c write
def else_write(command):
    global new_server
    global condition
    condition = 1
    new_server.new_ssh_write(command)

def create_threads(status='default'):
    global text_container
    global thread
    global thread_condition
    if status == 'default':
        thread_condition = 1
        thread = threading.Thread(target=info_update,args=(text_container,))
        thread.start()
    if status == 'stream':
        print("stream application active!")
        thread = threading.Thread(target=stream_screen,args=(text_container,))
        thread.start()

#1.03更新出的stream串流功能函数，可以直接调用
def stream_screen(text_container):
    global stream_vis
    while stream_vis:
        info = stream_client.visitor_get()
        text_container.config(state='normal')
        text_container.insert(tk.END, f'\n{info}')
        text_container.config(state='disabled')
        text_container.see(tk.END)

def check_event(keyboard_info,info,object):
    global condition
    global new_server
    global condition
    try:
        if keyboard_info == 'ctrl-c':
            else_write('\x03\n')
            print(keyboard_info)
        if keyboard_info == 'enter':
            container_write(info)
            info.delete(0,tk.END)
            history(status='entered')
        if keyboard_info == 'tab':
            command = info.get()
            new_server.new_ssh_write(command)
            time.sleep(0.5)
            new_server.new_ssh_write('\t')
            condition = 1
            for i in range (0,1024+1):
                new_server.new_ssh_write('\b')
        if keyboard_info == 'up':
            history('read','up',object)
        if keyboard_info == 'down':
            history('read','down',object)
        if keyboard_info == 'esc':
            else_write('\x1b')
    except Exception:
        pass

def history(status,info='',object=''):
    global history_lis
    global choose_num
    global first_condition
    try:
        if status == 'write':
            history_lis.append(info)
            print(history_lis)

        elif status == 'read':
            len_command = len(history_lis)

            if info == 'up':
                if first_condition == 1:
                    choose_num += 0
                else:
                    choose_num += 1
                if choose_num >= (len_command - 1):
                    choose_num = (len_command - 1)
                choose_command = history_lis[(len_command - 1) - choose_num]
                object.delete(0,tk.END)
                object.insert(tk.END,choose_command)
                print('up')
                first_condition += 1

            if info == 'down':
                choose_num -= 1
                if choose_num < 0:
                    choose_num = 0
                choose_command = history_lis[(len_command - 1) - choose_num]
                object.delete(0,tk.END)
                object.insert(tk.END,choose_command)
                print('down')

        elif status == 'entered':
            choose_num = 0
            first_condition = 1
    except Exception:
        pass

def sftp(status,ent_remote,ent_loacal):
    global new_server
    remote_path = ent_remote.get()
    local_path = ent_loacal.get()
    if status == 'download':
        new_server.download_files(remote_path,local_path)
    if status == 'upload':
        new_server.upload_files(remote_path,local_path)

#回收线程，空余对象
def del_all():
    global new_server
    global thread_condition
    global thread
    global stream_vis
    global root
    root.title('Connection Inactive')
    stream_vis = 0
    print(new_server)
    thread_condition = 0
    thread.join()
    del new_server
    init()

def del_host():
    global stream_host
    if stream_host == 1:
        stream_host = 0

def init():
    global history_lis
    global choose_num
    global first_condition
    global new_server
    global stream_host
    global stream_vis
    stream_host = 0
    stream_vis = 0
    choose_num = 0
    history_lis = []
    first_condition = 1
    new_server = 0

def insert_text(text_container,text):
    text_container.config(state='normal')
    text_container.insert(tk.END, f'\n{text}')
    text_container.config(state='disabled')
    text_container.see(tk.END)

def _hello():
    print(" ")
    print("/---------------------------------------------------\ ")
    print("|   作者/author   : EASTSTAR_YpMW                    |")
    print("|   这里是输出终端，非必要请勿关闭！                      |")
    print("|   This is info output Terminal                    |")
    print("|   版本/version  : V1.10                            |")
    print("\---------------------------------------------------/")
    print(" ")
    print(" ------------[Website:http://eaststar.ltd]------------ ")
    print(" ")


if __name__ == '__main__':
    _hello()
    new_server = 0
    main.init()
    init()
    inter = create_root()
    inter[0].mainloop()





