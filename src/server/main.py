import socket
from Giocatore import Giocatore
from Thread_partita import partita
import threading
import time
import sqlite3

def main():
    fase_di_gioco = "waiting"
    giocatori_seduti = []
    count = 0
    clients = []
    timeout = False

    # Configura il server
    server_host = '127.0.0.1'
    server_port = 12345

    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(6)
    server_socket.settimeout(10)
    while True:

        while not timeout:
            try:
                print(f"In attesa di connessioni su {server_host}:{server_port}...")
                client_socket, client_address = server_socket.accept()
                client_ip, client_port = client_address  # Estrai l'indirizzo IP e la porta

                print(f"Connessione da: {client_address}")

                # Ricevi i dati dal client
                data = client_socket.recv(1024)
                print(f"Dati ricevuti dal client: {data.decode('utf-8')}")

                # Decodifica i dati da bytes a stringa
                data_str = data.decode('utf-8')

                # Ora puoi usare il metodo split sulla stringa
                if data_str.split(";")[0] == "entry" and len(giocatori_seduti) < 6:
                    response = "ok;"
                    g = Giocatore(data_str.split(";")[1], 0, 0, 0, int(data_str.split(";")[2]), "no", "no", True, count, client_ip, client_port)
                    count += 1
                    clients.append((client_ip, client_port))
                    giocatori_seduti.append(g)
                    print(count)
                else:
                    response = "err"

                client_socket.send(response.encode('utf-8'))

            except socket.timeout:
                timeout = True
                server_socket.close()

            finally:
                try:
                    # Chiudi la connessione
                    if client_socket:
                        client_socket.close()
                except:
                    print("eccezione")

        if count >= 2:
            print("Inizio partita...")
            fase_di_gioco = "game"

            socket_partita = f"{server_host};888"
            for client_ip, client_port in clients:
                print(f"ip: {client_ip}; port: {client_port}")
                try:
                    # Crea un socket per la connessione al giocatore
                    giocatore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    giocatore_socket.connect((client_ip, client_port))
                    giocatore_socket.send(socket_partita.encode('utf-8'))
                    giocatore_socket.close()
                except Exception as e:
                    print(f"Errore durante la connessione al giocatore: {e}")

            # Crea un oggetto Thread
            thread = threading.Thread(target=partita, args=(fase_di_gioco,))

            # Avvia il thread
            thread.start()

            # Attendi che il thread termini prima di uscire
            thread.join()
            timeout = False
            count = 0
        

if __name__ == '__main__':
    main()