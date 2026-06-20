import socket

HOST, PORT = '', 8000

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))  
listen_socket.listen(1)  

print(f"サーバを起動しました。http://localhost:{PORT} でアクセスできます。")

while True:
    client_connection, client_address = listen_socket.accept()  
    request = client_connection.recv(1024).decode('utf-8') 
    print(request)

    http_response = """\
HTTP/1.1 200 OK

<html><body><h1>Hello, World!</h1></body></html>
"""
    client_connection.sendall(http_response.encode('utf-8'))  
    client_connection.close()  