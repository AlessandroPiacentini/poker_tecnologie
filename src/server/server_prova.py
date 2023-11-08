import socket
import time

# Crea un socket del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(6)



# Contatore per i messaggi ricevuti
message_count = 0

while True:
    try:
        # Accetta una connessione da un client
        client_socket, client_address = server_socket.accept()
        print(f"Connessione accettata da: {client_address}")

        # Ricevi il messaggio dal client
        message = client_socket.recv(1024).decode()
        print(f"Ricevuto: {message}")

        # Incrementa il contatore dei messaggi
        message_count += 1

        # Chiudi la connessione con il client
        client_socket.close()

        # Se abbiamo ricevuto più di 2 messaggi, esci dal ciclo
        if message_count >= 6:
            break
        if message_count >= 2:
            # Imposta il timeout sulla socket del server
            server_socket.settimeout(10)

    except socket.timeout:
        print("Timeout scaduto. Chiudo la socket.")
        break

# Chiudi la socket del server
server_socket.close()
