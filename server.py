import socket
import time

def processar_mensagem(mensagem, seq_num):
    print(f"[Servidor] Recebido pacote {seq_num}: '{mensagem}', tamanho {len(mensagem)} caracteres")
    
    if mensagem == mensagem[::-1]: # Já que no client estou invertendo pra simular um pacote corrupto, posso fazer isso para simular detecção
        print(f"[Servidor] Pacote {seq_num} CORROMPIDO! NACK!")
        return "NACK"
    return f"ACK: Mensagem {seq_num} recebida com sucesso!"

def servidor():
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[Servidor] Aguardando conexões em {host}:{port}...")

    client_socket, client_address = server_socket.accept()
    print(f"[Servidor] Conexão estabelecida com {client_address}")

    # Handshake inicial: Recebe configurações do cliente
    configuracao = client_socket.recv(1024).decode()
    modo_operacao, tamanho_maximo = configuracao.split(',')
    print(f"[Servidor] Configurações recebidas - Modo: {modo_operacao}, Tamanho máximo de pacote: {tamanho_maximo}")

    # Envia confirmação de recebimento das configurações
    client_socket.sendall(f"Configurações recebidas com sucesso! Modo: {modo_operacao}, Tamanho máximo: {tamanho_maximo}".encode())

    mensagem_completa = ""
    seq_num = 1

    while True:
        data = client_socket.recv(3)  # Recebe pacotes de tamanho máximo 3 caracteres
        if not data:
            break
        
        mensagem = data.decode()
        if mensagem == "FIM":
            break

        mensagem_completa += mensagem
        metadados_resposta = processar_mensagem(mensagem, seq_num)
        
        client_socket.sendall(metadados_resposta.encode())
        
        seq_num += 1

    if len(mensagem_completa) == 0:
        print(f"\n[Servidor] Mensagem vazia")
    else:
        print(f"\n[Servidor] Mensagem completa recebida: {mensagem_completa}")
    
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    servidor()
