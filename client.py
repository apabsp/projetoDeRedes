import socket
import time

# Cliente deve se conectar ao servidor via localhost
comando = input("Selecione tipo de conexão. (GET, POST...) ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # af_net = protocolo iPv4, sock_stream = TCP

server_address = ('localhost', 80)  # Definindo o localhost

# Colocar uma lógica de retry para conexão com host
retries = 5
for i in range(retries):
    try:
        s.connect(server_address)  # Tenta a conexão
        break 
    except ConnectionRefusedError:
        print(f"Connection failed, retrying ({i + 1}/{retries})...")
        time.sleep(2)  # Espera 2 segundos antes de tentar novamente
else:
    print("Failed to connect after several attempts.")
    exit(1)

print("Enviando comando:", comando)
s.sendall((comando+"\n").encode())  # Envia o comando para o servidor com newLine
print("Comando Enviado.")

while True:
    
    data = s.recv(512)  # Aguarda receber dados do servidor (até 512 bytes por vez)
    #print(f"Recebido: {data}")  # Debug
    if len(data) < 1:
        print("\n\n\nNenhum dado restando para receber!")
        break
    print(data.decode(), end="")


s.close()
print("\nConexão encerrada!")