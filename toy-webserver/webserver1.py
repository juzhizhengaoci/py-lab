import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))

    # HTTP 报文规范：行结束符必须是 CRLF（\r\n），不是单独的 \n；
    # 状态行与响应头之后、响应体之前，用一个空行（连续两个 CRLF）分隔。
    body = b'Hello, World!'
    http_response = (
        b'HTTP/1.1 200 OK\r\n'
        b'Content-Type: text/plain; charset=utf-8\r\n'
        b'Content-Length: ' + str(len(body)).encode('ascii') + b'\r\n'
        b'Connection: close\r\n'
        b'\r\n'
        + body
    )

    client_connection.sendall(http_response)
    client_connection.close()
