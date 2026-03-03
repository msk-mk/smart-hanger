import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 12345
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print('[*] listen {}:{}'.format(bind_ip, bind_port))

def handle_client(client_socket):
    bufsize=1024
    while True:
        request = client_socket.recv(bufsize)
        print('[*] recv: {}' .format(request.decode()))
        client_socket.send(b"Hey Client!\r\n")

while True:
    client,addr = server.accept()
    print('[*] connected from: {}:{}'.format(addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()