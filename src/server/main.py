import socket
from Player import Player
from condivisa import set_info, SingletonClass
from Thread_game import game
from Thread_waiting import waiting
import os
import threading


        
# Define common variable
game_phase = "waiting"
seated_players = []
winner_index = 0

# Create a Lock object
lock = threading.Lock()
server_host = ""
server_port = 0
timeout = False
clients = []

server_socket=None


count_player = 0



def set_ip_server():
    global server_host
    global server_port
    
    try:
        f= open("config.csv", "r") 
        line = f.readline().split(":")
        if len(line) >= 3:
            server_host = line[1].strip()  # Rimuovi spazi bianchi extra
            server_port = int(line[2].strip())
        else:
            print("Il file di configurazione non ha abbastanza elementi.")
    except FileNotFoundError:
        print("Il file di configurazione non è stato trovato.")
        server_host = "127.0.0.1"  # Rimuovi spazi bianchi extra
        server_port = 1234
    except ValueError:
        print("Errore nella conversione del numero di porta in un intero.")
    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {e}")

        
          
def attendi_nuove_connessioni():
    """
    Wait for new client connections.

    This function listens for new client connections on the server socket and
    accepts them. It assigns the client socket to the corresponding player object
    in the seated_players list.

    Args:
        None

    Returns:
        None
    """
    global server_host
    global server_port
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_port=888
    server_socket.bind((server_host, _server_port))
    server_socket.listen(6)
    i=0
    print (len(seated_players))
    while i<len(seated_players):
        print(f"Waiting for connections on secoda volta{server_host}:{server_port}...")
        client_socket, client_address = server_socket.accept()

        print(f"Connection from: {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024)
        print(f"Data received from the client: {data.decode('utf-8')}")

        # Decode data from bytes to string
        data_str = data.decode('utf-8')
        
        if(data_str=="connesso"):
            seated_players[i].client_socket=client_socket
            
            i+=1
            
            
            
def main():
    """
    The main function that runs the server and handles client connections.

    This function creates a TCP/IP socket, binds it to a specific host and port,
    and listens for incoming client connections. It receives data from the client,
    processes it, and sends a response back. If the number of seated players is
    less than 6, it allows the client to join the game. Once there are at least
    2 players, it starts the game by connecting to each player and sending the
    necessary game information. It also creates and starts two threads for handling
    the game and waiting for players to join.

    Args:
        None

    Returns:
        None
    """
    global seated_players 
    global clients 
    global timeout
    global count_player
    # Configure the server
    global server_host
    global server_port
    
    set_ip_server()
    while True:
        
        global server_socket
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_host, server_port))
        server_socket.listen(6)
        seated_players=[]

        while not timeout:
            try:
                print(f"Waiting for connections on {server_host}:{server_port}...")
                client_socket, client_address = server_socket.accept()

                print(f"Connection from: {client_address}")

                # Receive data from the client
                data = client_socket.recv(1024)
                print(f"Data received from the client: {data.decode('utf-8')}")

                # Decode data from bytes to string
                data_str = data.decode('utf-8')

                # Now you can use the split method on the string
                if data_str.split(";")[0] == "entry" and len(seated_players) < 6:
                    count_player += 1
                    response = f"ok;{count_player}"
                    player = Player(data_str.split(";")[1], 0, 0, 0, int(data_str.split(";")[2]), "no", "no", True, count_player, client_socket)
                    clients.append(client_socket)
                    seated_players.append(player)
                    print(count_player)
                    if(count_player>=2):
                        server_socket.settimeout(10)
                else:
                    response = "err"

                client_socket.send(response.encode('utf-8'))

            except socket.timeout:
                timeout = True
                # server_socket.close()

            

        if count_player >= 2:
            print("Starting the game...")
            global game_phase
            game_phase="game"
            socket_game = f"{server_host};888"
            for client_socket_ in clients:
                print(" Connecting to the player...")
                try:
                    # Create a socket for connecting to the player
                    # player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # player_socket.connect(client_address)
                    client_socket_.sendall(socket_game.encode('utf-8'))
                except Exception as e:
                    print(f"Error connecting to the player: {e}")
                    
            print("socket inviata")
            attendi_nuove_connessioni()
            


            # Crea un oggetto Thread
            set_info(seated_players, game_phase, winner_index, count_player, server_socket)
            
            
            thread_partita = threading.Thread(target=game)
            thread_waiting= threading.Thread(target=waiting)
       

            # Start the thread
            thread_partita.start()
            thread_waiting.start()

            # Wait for the thread to finish before exiting
            thread_partita.join()
            thread_waiting.join()
            print("Fake")
            clients=[]
            timeout = False
            count_player = 1
            
        server_socket.close()
            

if __name__ == '__main__':
    main()


  