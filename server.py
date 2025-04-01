import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('localhost', 80)
server_socket.bind(server_address)


server_socket.listen(1)
print("Socket escuta...")

while True:
    print("Aguardando conexão")
    connection, client_address = server_socket.accept() # The return value is a pair (conn, address)
    #conn is a new socket object usable to send and receive data on the connection
    #address is the address bound to the socket on the other end of the connection.

    try:
        print("Conectado a ", client_address)
        data = connection.recv(512)
        if data:
            comando = data.decode().strip()
            print("Comando recebido:", comando)
            
            if comando == "GET":
                resposta = "OK - Dados recebidos com sucesso!\n"
                connection.sendall(resposta.encode())
            elif comando == "POST":
                resposta = "Comando POST não implementado ainda\n"
            else:
                resposta = "ERRO - Comando não reconhecido\n"
            
    except:
        print("Algo de errado aconteceu.")
    connection.close()