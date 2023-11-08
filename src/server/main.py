import socket
from Giocatore import Giocatore
import Thread_partita
import threading
from Thread_partita import partita
import time



def main():
    fase_di_gioco="waiting"
    giocatori_seduti=[]
    giocatori_vivi=[]
    soldi_banco=0
    carte_sul_banco=[]
    count=0
    timer=0
    
    
    
    
    # Configura il server
    server_host = '127.0.0.1'  # Indirizzo IP del server
    server_port = 12345  # Porta del server

    
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa il socket all'indirizzo e alla porta del server
    server_socket.bind((server_host, server_port))

    # Ascolta le connessioni in arrivo (massimo 1 connessione in coda)
    server_socket.listen(6)
    while True:        
        try:
            

            print(f"In attesa di connessioni su {server_host}:{server_port}...")
            client_socket, client_address = server_socket.accept()
            print(f"Connessione da: {client_address}")

            # Ricevi i dati dal client
            data = client_socket.recv(1024)
            print(f"Dati ricevuti dal client: {data.decode('utf-8')}")


            # Decodifica i dati da bytes a stringa
            data_str = data.decode('utf-8')

            # Ora puoi usare il metodo split sulla stringa
            if data_str.split(";")[0] == "entry" or giocatori_seduti.count<6:
                response="ok;"
                g= Giocatore(data_str.split(";")[1], [],0,int(data_str.split(";")[2]) , "no","no", True, count, client_socket)
                count+=1
                giocatori_seduti.append(g)
                if giocatori_seduti.count >=2:
                    # Imposta il timeout sulla socket del server
                    server_socket.settimeout(10)
            else:
                response="err"
            client_socket.send(response.encode('utf-8'))
        except:
            # Chiudi la connessione
            client_socket.close()
            server_socket.close()
            
            #timer inizio partita
            if timer==10 :
                timer=0
                fase_di_gioco="game"
                
            #inizio game
            if fase_di_gioco=="game" :
                for giocatore in giocatori_seduti:
                    socket_partita=f"{server_host};888"
                    giocatore.socket.send(socket_partita.encode('utf-8'))
                    giocatore.socket.close()
                # Crea un oggetto Thread
                thread = threading.Thread(target=partita, args=(giocatori_seduti, fase_di_gioco))

                # Avvia il thread
                thread.start()

                # Attendi che il thread termini prima di uscire
                thread.join()


if __name__=='__main__':
    main()
