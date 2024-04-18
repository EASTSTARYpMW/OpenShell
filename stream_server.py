import socket
import threading

def man_get(client,addr=''):
    global _host
    global _visitor
    info = client.recv(1024).decode('utf-8')
    if info == 'host':
        _host = 2
        print(f'{addr}  host ready.')
    if info == 'visitor':
        _visitor = 1
        print(f"{addr}  visitor ready")
    if _host + _visitor == 3:
        print("Host and Visitor has connected")
        info_interchange(status=info,client=client)

def info_interchange(status,client):
    if status == 'host':
        while True:
            global host_info
            global update_
            host_info = client.recv(1024).decode('utf-8')
            print(f'host :{host_info}')
            update_ = 1
            pass
    if status == 'visitor':
        if update_ == 1:
            while True:
                client.send(host_info.encode('utf-8'))
                update_ = 0

def init():
    global _host
    global _visitor
    global host_info
    global update_
    update_ = 0
    host_info = 0
    _host = 0
    _visitor = 0

def accept_connect(stream_socket):
    while True:
        client,addr = stream_socket.accept()
        client_thread = threading.Thread(target=man_get,args=(client,addr))
        client_thread.start()

if __name__ == '__main__':
    print('Running')
    init()
    stream_socket = socket.socket()
    stream_socket.bind(('0.0.0.0',7860))
    stream_socket.listen(5)
    accept_connect(stream_socket)


