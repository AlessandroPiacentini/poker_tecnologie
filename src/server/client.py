import socket

# Indirizzo IP e porta del server
server_ip = '127.0.0.1'
server_port = 12345  # Sostituisci con la porta del server

# Crea una connessione al server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Messaggio da inviare al server
message = "entry;prova;100"

# Invia il messaggio al server
client_socket.sendall(message.encode())

# Ricevi la risposta dal server
response = client_socket.recv(1024)  # Ricevi fino a 1024 byte di dati

# Decodifica la risposta
response_str = response.decode()

# Stampa la risposta del server
print("Risposta dal server:", response_str)

# Chiudi la connessione al server
client_socket.close()

server_port = 54322

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Associa il socket all'indirizzo e alla porta del server
server_socket.bind((server_ip, server_port))

# Ascolta le connessioni in arrivo (massimo 1 connessione in coda)
server_socket.listen(6)
server_socket.settimeout(30)
print(f"In attesa di connessioni su {server_ip}:{server_port}...")
client_socket, client_address = server_socket.accept()
print(f"Connessione da: {client_address}")

# Ricevi i dati dal client
data = client_socket.recv(1024)
print(f"Dati ricevuti dal client: {data.decode('utf-8')}")
