import socket
import time
import random

# Simulação de falhas nos pacotes
def simular_falhas(pacote, seq_num):
    # Probabilidade de perda de pacote (por exemplo, 10%)
    if random.random() < 0.1:
        print(f"[Cliente] Pacote {seq_num} perdido (simulação de perda de pacote).")
        return None  # Simula a perda do pacote (não envia)
    
    # Probabilidade de corrupção de pacote (por exemplo, 10%)
    if random.random() < 0.1:
        pacote_corrompido = pacote[::-1]  # Inverte o pacote para simular corrupção
        print(f"[Cliente] Pacote {seq_num} corrompido (conteúdo alterado).")
        return pacote_corrompido
    
    return pacote

def cliente():
    host = 'localhost'
    port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Protocolo IPv4 e TCP
    s.connect((host, port))

    mensagem_completa = input("Digite a mensagem completa para enviar: ")
    
    pacotes = [mensagem_completa[i:i+3] for i in range(0, len(mensagem_completa), 3)]
    
    seq_num = 1
    for pacote in pacotes:
        # Envio do pacote com simulação de falha
        while True:
            print(f"[Cliente] Enviando pacote {seq_num}: '{pacote}', tamanho {len(pacote)} caracteres")
            
            pacote_modificado = simular_falhas(pacote, seq_num)
            if pacote_modificado is None:
                # Simulando a perda de pacote. Espera e tenta novamente.
                time.sleep(1)  # Espera 1 segundo para simular o atraso de perda
                continue

            # Envia o pacote para o servidor
            s.sendall(pacote_modificado.encode())
            
            # Espera a resposta do servidor
            resposta = s.recv(1024).decode()
            
            # Se o pacote foi corrompido, o servidor pode perceber isso e enviar um NACK
            if "NACK" in resposta:
                print(f"[Cliente] Pacote {seq_num} corrompido, tentando novamente...")
                continue  # Tenta novamente o envio desse pacote

            print(f"[Cliente] Recebido do servidor: {resposta}")
            break  # Se tudo deu certo, sai do loop e passa para o próximo pacote
        seq_num += 1

    # Envia uma mensagem de fim para finalizar a comunicação
    s.sendall("FIM".encode())
    print("[Cliente] Comunicação finalizada.")
    
    # Fecha a conexão
    s.close()

if __name__ == "__main__":
    cliente()
