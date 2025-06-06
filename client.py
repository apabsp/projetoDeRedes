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

''' Se quiser testar corrompido
    pacote_corrompido = pacote[::-1]
    print(f"[Cliente] Pacote {seq_num} corrompido (forçado).")
    return pacote_corrompido
'''

def cliente():
    host = 'localhost'
    port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Protocolo IPv4 e TCP
    s.connect((host, port))

    # Handshake inicial: Cliente envia configurações para o servidor
    modo_operacao = "Go-Back-N"  # Exemplo de modo de operação
    tamanho_maximo = 3  # Tamanho máximo de pacote
    s.sendall(f"{modo_operacao},{tamanho_maximo}".encode())
    
    # Espera a confirmação do servidor
    resposta = s.recv(1024).decode()
    print(f"[Cliente] Configuração recebida do servidor: {resposta}")

    simularPerda = input("\nDeve simular a perda de pacotes? (s / n) ")
    while simularPerda.lower() != "s" and simularPerda.lower() != "n":
        simularPerda = input("\nInput inválido. Deve simular a perda de pacotes? (s / n) ")
    simularPerda = True if simularPerda.lower() == "s" else False


    # Envia a mensagem completa para o servidor
    mensagem_completa = input("Digite a mensagem completa para enviar: ")
    
    pacotes = [mensagem_completa[i:i+3] for i in range(0, len(mensagem_completa), 3)]
    
    seq_num = 1
    for pacote in pacotes:
        while True:
            print(f"[Cliente] Enviando pacote {seq_num}: '{pacote}', tamanho {len(pacote)} caracteres")
            
            pacote_modificado = simular_falhas(pacote, seq_num) if simularPerda else pacote # Dependendo se o usuário quer simular falhas.
            if pacote_modificado is None:
                time.sleep(1)  # Espera 1 segundo para simular o atraso de perda
                continue


            #Aqui simulamos um atraso com random
            atraso = random.uniform(0.5, 5.0)
            print(f"[Cliente] Atraso de {atraso:.2f}s antes do envio do pacote {seq_num}")
            s.sendall(pacote_modificado.encode())

            if random.random() < 0.1: # Simular duplicação, deixar o servidor resolver
                print(f"[Cliente] Enviando pacote {seq_num} novamente (duplicata).")
                s.sendall(pacote_modificado.encode())
            
            resposta = s.recv(1024).decode()
            
            if "NACK" in resposta:
                print(f"[Cliente] Pacote {seq_num} corrompido ou com erro, tentando novamente...")
                continue  # Tenta novamente o envio desse pacote

            print(f"[Cliente] Recebido do servidor: {resposta}")
            break  # Se tudo deu certo, sai do loop e passa para o próximo pacote
        seq_num += 1

    s.sendall("FIM".encode())
    print("[Cliente] Comunicação finalizada.")
    s.close()

if __name__ == "__main__":
    cliente()
