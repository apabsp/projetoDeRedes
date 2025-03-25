import socket

#https://docs.python.org/3/library/socket.html

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #first parameter specifies IPv4, second parameter specifies TCP
mysocket.connect(('google.com', 80)) # port
comando = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

mysocket.sendall(comando.encode())  # fix

while True:
    data = mysocket.recv(512) 
    if len(data) < 1:
        break
    print(data.decode(), end="")

mysocket.close()