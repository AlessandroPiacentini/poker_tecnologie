import socket

# Configura il client
server_host = '127.0.0.1'  # Indirizzo IP del server
server_port = 12345  # Porta del server

# Crea un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connettiti al server
client_socket.connect((server_host, server_port))

# Invia un messaggio al server
message = "entry;prova;10"
client_socket.send(message.encode('utf-8'))

# Ricevi la risposta dal server
response = client_socket.recv(1024)
print(f"Risposta dal server: {response.decode('utf-8')}")

# Chiudi la connessione
client_socket.close()



# Configura il server
server_host = '127.0.0.1'  # Indirizzo IP del server
server_port = 56321  # Porta del server

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa il socket all'indirizzo e alla porta del server
server_socket.bind((server_host, server_port))

# Ascolta le connessioni in arrivo (massimo 1 connessione in coda)
server_socket.listen(6)
print(f"In attesa di connessioni su {server_host}:{server_port}...")
client_socket, client_address = server_socket.accept()
print(f"Connessione da: {client_address}")
# Ricevi i dati dal client
data = client_socket.recv(1024)
print(f"Dati ricevuti dal client: {data.decode('utf-8')}")
client_socket.close()
server_socket.close()
