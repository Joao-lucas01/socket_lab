import socket

HOST = "127.0.0.1"
PORT = 9000
TIMEOUT_SEGUNDOS = 3.0

try:
    print(f"[CLIENTE] Conectando a {HOST}:{PORT} com timeout de {TIMEOUT_SEGUNDOS}s...")
    # Cria conexão com timeout definido
    client = socket.create_connection((HOST, PORT), timeout=TIMEOUT_SEGUNDOS)
    
    print("[CLIENTE] Enviando 'ping'...")
    client.sendall(b"ping")
    
    # Aguarda resposta
    resposta = client.recv(64).decode()
    print(f"[CLIENTE] Resposta recebida: '{resposta}'")
    
    client.close()

except socket.timeout:
    print("[ERRO - TIMEOUT] O servidor demorou mais que o limite para responder (falha parcial / travamento).")
except ConnectionRefusedError:
    print("[ERRO - CONNECTION REFUSED] O servidor nao esta ativo na porta informada.")
except ConnectionResetError:
    print("[ERRO - CONNECTION RESET] O servidor encerrou a sessao abruptamente.")
except Exception as e:
    print(f"[ERRO GENÉRICO]: {e}")