import socket, time

message = 'hello'
host = '127.0.0.1'

#Client
client_socket = socket.socket()
client_socket.connect((host, 10000))
client_socket.send(message.encode("utf-8"))
reply = client_socket.recv(1024).decode()
print(reply)
client_socket.close()



