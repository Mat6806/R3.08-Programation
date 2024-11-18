import socket, time
host = '127.0.0.1'
reply = "hello"

#Serveur
server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 10000))
server_socket.listen(1)
conn, address = server_socket.accept()
message = conn.recv(1024).decode()
conn.send(reply.encode("utf-8"))
print(message)
conn.close()
server_socket.close()
