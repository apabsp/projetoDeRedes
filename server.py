import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 80)
server_socket.bind(server_address)

server_socket.listen(1)
print("Socket escuta...")

while True:
    print("Aguardando conexão")
    connection, client_address = server_socket.accept()  # O retorno é um par (conn, address)
    
    try:
        print("Conectado a ", client_address)
        data = connection.recv(512)
        if data:
            comando = (data.decode().strip()).upper()
            print("Comando recebido:", comando)
            
            if comando == "GET":
                resposta = "OK - Dados recebidos com sucesso!\n"
                print(f"Enviando resposta: {resposta}")
                connection.sendall(resposta.encode())  # Envia a resposta
            elif comando == "POST":
                resposta = "Comando POST não implementado ainda\n"
                print(f"Enviando resposta: {resposta}")
                connection.sendall(resposta.encode())
            else:
                resposta = "ERRO - Comando não reconhecido\n"
                print(f"Enviando resposta: {resposta}")
                connection.sendall(resposta.encode())
        else:
            print("Nenhum dado recebido.")
    except Exception as e:
        print(f"Algo deu errado: {e}")
    finally:
        connection.close()
