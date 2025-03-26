import socket

#https://docs.python.org/3/library/socket.html

#O cliente deve ser capaz de se conectar ao servidor através do localhost
#(quando na mesma máquina) ou via IP. A comunicação deve ocorrer via sockets;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #af_net = protocolo iPv4, sock_stream = TCP

server_address = ('', 80) #definição do localhost
s.connect(server_address) #conexão com o host

s.sendall(comando.encode())  #envia o get pro servidor

while True:
    data = s.recv(512) #leitura dos bytes
    if len(data) < 1:
        break
    print(data.decode(), end="")

s.close()

# Um protocolo de aplicação (regras a nível de aplicação) deve ser proposto e
# descrito (requisições e respostas descritas);