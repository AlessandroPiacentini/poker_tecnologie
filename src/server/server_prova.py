import socket
import threading
import time

# Definisci una funzione per gestire ciascun client
def handle_client(client_socket, client_address):
    print(f"Connessione da: {client_address}")
    clients.append((client_socket, client_address))

# Indirizzo IP e porta del server
server_ip = '127.0.0.1'
server_port = 12345

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa il socket all'indirizzo e alla porta del server
server_socket.bind((server_ip, server_port))

# Ascolta le connessioni in arrivo (massimo 2 connessioni in coda)
server_socket.listen(2)

print(f"In attesa di connessioni su {server_ip}:{server_port}...")

clients = []

# Accetta almeno due connessioni dai client
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

# Dopo 10 secondi, invia un messaggio ai client
time.sleep(10)
message = "Messaggio daierver dopo 10 secondi"
for client, _ in clients:
    client.send(message.encode('utf-8'))

# Chiudi tutte le connessioni
for client, _ in clients:
    client.close()

# Chiudi il socket del server
server_socket.close()
