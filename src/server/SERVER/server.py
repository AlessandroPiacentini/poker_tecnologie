import socket
import threading

clients = 0

def handle_client(client_socket, shared_message, shutdown_event):
    global clients
    try:
        # Ciclo per gestire la comunicazione con il client
        while not shutdown_event.is_set():
            data = client_socket.recv(1024)
            if not data:
                break

            received_message = data.decode()
            parts = received_message.split(';')
            print("Parti del messaggio:", parts)
            
            # Se il messaggio inizia con "entrare", incrementa il contatore dei client
            if received_message.split(';')[0].strip() == "entrare":
                clients += 1
                confirm_message = "connesso\r\n"
                print(f"Invio: {confirm_message}")
                client_socket.sendall(confirm_message.encode())
            # Se il messaggio inizia con "Inizio_Carte", invia un messaggio di conferma
            elif received_message.split(';')[0].strip() == "Inizio_Carte":
                confirm_message = "12;12"
                client_socket.sendall(confirm_message.encode())
            else:
                # Se il messaggio non corrisponde a nessuna condizione, invia un messaggio di errore
                other_message = "no"
                client_socket.sendall(other_message.encode())
                print(f"Errore non funzica: {received_message}")

                # Setta la variabile condivisa
                shared_message.set(received_message)
            
    except Exception as e:
        print(f"Errore durante la gestione del client: {e}")

    finally:
        # Chiudi il socket del client quando hai finito
        client_socket.close()

def send_messages(shared_message, shutdown_event):
    try:
        # Ciclo per gestire l'invio dei messaggi ai client
        while not shutdown_event.is_set():
            # Attendere fino a quando un nuovo messaggio è disponibile
            if shared_message.wait(timeout=1):
                # Ottenere il messaggio e reimpostare la variabile condivisa
                server_message = shared_message.get()
                shared_message.clear()

                # Puoi fare ciò che vuoi con il messaggio del server
                print(f"Ricevuto messaggio dal client: {server_message}")

    except Exception as e:
        print(f"Errore durante la gestione dei messaggi: {e}")

def listen_for_clients(server_socket, shared_message, shutdown_event):
    try:
        # Ciclo per accettare nuove connessioni dai client
        while not shutdown_event.is_set():
            client_socket, client_address = server_socket.accept()
            print(f"Connessione accettata da {client_address}")

            # Avvia un thread per gestire il client appena connesso
            client_thread = threading.Thread(target=handle_client, args=(client_socket, shared_message, shutdown_event))
            client_thread.start()

    except Exception as e:
        print(f"Errore durante l'ascolto dei client: {e}")

def main():
    # Impostazioni del server
    server_address = "localhost"
    server_port = 666

    # Creazione del socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen()

    print(f"Server in ascolto su {server_address}:{server_port}")

    # Creazione degli oggetti per la gestione del messaggio condiviso e dell'evento di chiusura
    shared_message = threading.Event()
    shutdown_event = threading.Event()

    try:
        # Avvia il thread per accettare connessioni dai client
        listen_thread = threading.Thread(target=listen_for_clients, args=(server_socket, shared_message, shutdown_event))
        listen_thread.start()

        # Avvia il thread per inviare messaggi ai client
        send_thread = threading.Thread(target=send_messages, args=(shared_message, shutdown_event))
        send_thread.start()

        # Attendere la chiusura del thread di ascolto
        listen_thread.join()

    except KeyboardInterrupt:
        print("Server terminato manualmente.")
    
    finally:
        # Imposta l'evento di chiusura e chiudi il socket del server
        shutdown_event.set()
        server_socket.close()

if __name__ == "__main__":
    main()
