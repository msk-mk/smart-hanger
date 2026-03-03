import socket

HOST, PORT = '', 8000

# ソケットを作成
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))  # ホスト名とポート番号を指定
listen_socket.listen(1)  # 最大接続数を指定

print(f"サーバを起動しました。http://localhost:{PORT} でアクセスできます。")

while True:
    client_connection, client_address = listen_socket.accept()  # クライアントからの接続を待つ
    request = client_connection.recv(1024).decode('utf-8')  # クライアントからのリクエストを受信
    print(request)

    # HTTPレスポンスを作成
    http_response = """\
HTTP/1.1 200 OK

<html><body><h1>Hello, World!</h1></body></html>
"""
    client_connection.sendall(http_response.encode('utf-8'))  # レスポンスをクライアントに送信
    client_connection.close()  # 接続を閉じる