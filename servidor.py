import socket
import time

HOST = "127.0.0.1"
PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)
print(f"[SERVIDOR] Escutando em {HOST}:{PORT}...")

conn, addr = s.accept()
print(f"[SERVIDOR] Conectado por: {addr}")

msg = conn.recv(64).decode()
print(f"[SERVIDOR] Mensagem recebida: '{msg}'")

# Necessário descomentar a linha abaixo para fazer o teste do TIMEOUT no cliente:
# time.sleep(10)

conn.send(b"pong")
print("[SERVIDOR] 'pong' enviado. Fechando conexao.")
conn.close()
s.close()

