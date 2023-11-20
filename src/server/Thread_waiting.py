from main import fase_di_gioco, lock, giocatori_seduti, count
from Giocatore import Giocatore
import socket
import threading

# Inizializza il vettore per i messaggi
giocatori_seduti = []
max_messages = 6

# Funzione che gestisce la connessione di un client
def handle_client(client_socket, address, client_ip, client_port):
    global giocatori_seduti

    print(f"Connessione accettata da {address}")

    while True:
        # Ricevi dati dal client
        data = client_socket.recv(1024)
        if not data:
            break  # Se il client chiude la connessione, esci dal ciclo

       
        # Verifica se il vettore supera la lunghezza massima
        if len(giocatori_seduti) >= max_messages:
            response = "tavolo pieno"
            client_socket.send(response.encode("utf-8"))
            print(response)
            break
        else:
            # Decodifica e salva il messaggio nel vettore
            message = data.decode("utf-8")
            g=Giocatore(message.split(";")[1], 0, 0, 0, int(message.split(";")[2]), "no", "no", True, count, client_ip, client_port)
            giocatori_seduti.append(g)

        print(f"Ricevuto messaggio: {message}")

    # Chiudi la connessione con il client
    client_socket.close()
    print(f"Connessione chiusa con {address}")



def waiting():
    # Configura il server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)

    print("Server in ascolto su 127.0.0.1:12345")

    # Accetta connessioni dai client
    while fase_di_gioco=="game":
        client_socket, client_address = server.accept()
        client_ip, client_port = client_address

        handle_client(client_socket, client_address, client_ip, client_port)
