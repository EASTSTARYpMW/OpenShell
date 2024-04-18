import socket

# host = 'eaststar.ltd'
# port = 7860

def establish_hostman(server_url,port):
    global hostman_stream
    info = 'host'
    port = int(port)
    hostman_stream = socket.socket()
    server_address = (server_url,port)
    hostman_stream.connect(server_address)
    hostman_stream.send(info.encode('utf-8'))
    print('Connect to host Successfully')

def host_send(info):
    global hostman_stream
    hostman_stream.send(info.encode('utf-8'))

def visitor_get():
    global visitor_stream
    info = visitor_stream.recv(1024).decode('utf-8')
    return info

def establish_visitor(server_url,port):
    global visitor_stream
    info = 'visitor'
    port = int(port)
    visitor_stream = socket.socket()
    server_address = (server_url, port)
    visitor_stream.connect(server_address)
    visitor_stream.send(info.encode('utf-8'))
    print('Connect to host Successfully')

if __name__ == '__main__':
    print("please start program!")
    
    