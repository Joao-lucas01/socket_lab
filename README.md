# Lab 01 — Sockets TCP e Falhas Parciais
**Disciplina:** Sistemas Distribuídos  
**Aluno:** João Lucas - RA N296240
**Professor:** Janderson Borges  

> **Nota de transparência:** Este laboratório foi desenvolvido por mim com apoio de IA como ferramenta de consulta/revisão. O código foi testado localmente no terminal e a documentação abaixo reflete o meu entendimento prático dos conceitos.

---

## 1. O que foi feito

Construí um par de scripts em Python (`servidor.py` e `cliente.py`) para testar comunicação básica via socket TCP (troca de mensagens `ping` e `pong`) e, principalmente, simular o que acontece quando a rede ou o servidor falham.

### Estrutura dos arquivos:
* `servidor.py`: Abre a porta 9000 em `127.0.0.1`, aguarda conexão, recebe a string `ping`, responde com `pong` e encerra.
* `cliente.py`: Conecta no servidor usando `socket.create_connection` com um **timeout explícito de 3 segundos** e faz o tratamento de exceções.

---

## 2. Como rodar os testes

Abra dois terminais na pasta do projeto.

### Teste 1: Fluxo Normal (Ping-Pong)
1. Terminal 1: `python3 servidor.py`
2. Terminal 2: `python3 cliente.py`
* **Resultado:** O servidor recebe `ping`, o cliente recebe `pong` e ambos finalizam sem erro.

### Teste 2: Erro Imediato (`ConnectionRefusedError`)
1. Garanta que o `servidor.py` **não** esteja rodando.
2. Terminal 2: `python3 cliente.py`
* **O que acontece:** O sistema operacional local tenta bater na porta 9000, vê que não tem nenhum processo escutando e devolve na hora um pacote TCP `RST` (Reset). O Python captura isso como `ConnectionRefusedError`. O cliente sabe imediatamente que a conexão falhou.

### Teste 3: Falha Silenciosa / Timeout (`socket.timeout`)
1. No `servidor.py`, descomente a linha `time.sleep(10)` (simula um travamento ou lentidão extrema após aceitar a conexão).
2. Terminal 1: `python3 servidor.py`
3. Terminal 2: `python3 cliente.py`
* **O que acontece:** O cliente conecta e manda o `ping`, mas o servidor fica travado no sleep. O cliente não recebe nada e não tem como saber se o servidor morreu ou se a rede caiu. Passados os 3 segundos configurados, o cliente desiste e estoura `socket.timeout`.

---

## 3. Respostas das Questões Teóricas

### 3.1. Timeout vs. Erro de Conexão: qual a diferença na prática?
* **Erro de Conexão (`ConnectionRefusedError`):** É uma falha **explícita e imediata**. A máquina de destino responde ativamente dizendo "não há ninguém ouvindo nessa porta".
* **Timeout (`socket.timeout`):** É uma falha **silenciosa / parcial**. A rede ou o processo remoto param de responder sem mandar nenhum aviso de encerramento (`FIN` ou `RST`). Sem um timeout configurado, o cliente ficaria travado para sempre esperando uma resposta que nunca vai chegar.

### 3.2. Diferença entre `127.0.0.1` e `0.0.0.0`
* **`127.0.0.1` (Loopback):** O socket fica amarrado apenas à interface interna da própria máquina. Ninguém de fora (outros PCs na mesma rede) consegue conectar.
* **`0.0.0.0` (Todas as interfaces):** O servidor escuta em todas as placas de rede disponíveis (loopback, cabo de rede, Wi-Fi). É o que permite que outras máquinas façam requisições ao servidor.

---

## 4. As 3 Propriedades de Sistemas Distribuídos Observadas

1. **Concorrência e Processos Independentes:**  
   Cliente e servidor são dois processos totalmente separados. Eles não compartilham memória nem estado, comunicando-se apenas via fluxo de bytes pela rede.

2. **Sem Relógio Global:**  
   O cliente não sabe o tempo interno do servidor nem quanto tempo o servidor vai levar para processar algo. Por isso, a contagem do timeout precisa ser controlada localmente pelo próprio cliente.

3. **Falhas Parciais:**  
   Um dos nós (o servidor) pode travar ou congelar sem que o outro (o cliente) quebre junto. O cliente precisa ser programado com proteções (try/except e timeouts) para continuar vivo mesmo quando a outra ponta falha.