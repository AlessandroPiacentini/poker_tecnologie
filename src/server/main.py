import socket
from Player import Player
from Thread_game import game
# from Thread_waiting import waiting
import threading
import time
import sqlite3

# Define common variable
game_phase = "waiting"
seated_players = []
winner_index = 0

# Create a Lock object
lock = threading.Lock()


count = 0
def main():
    global seated_players 
    clients = []
    timeout = False
    global count
    # Configure the server
    server_host = '127.0.0.1'
    server_port = 12345

    while True:
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_host, server_port))
        server_socket.listen(6)
        seated_players=[]

        while not timeout:
            try:
                print(f"Waiting for connections on {server_host}:{server_port}...")
                client_socket, client_address = server_socket.accept()
                client_ip, client_port = client_address  # Extract the IP address and port

                print(f"Connection from: {client_address}")

                # Receive data from the client
                data = client_socket.recv(1024)
                print(f"Data received from the client: {data.decode('utf-8')}")

                # Decode data from bytes to string
                data_str = data.decode('utf-8')

                # Now you can use the split method on the string
                if data_str.split(";")[0] == "entry" and len(seated_players) < 6:
                    count += 1
                    response = f"ok;{count}"
                    player = Player(data_str.split(";")[1], 0, 0, 0, int(data_str.split(";")[2]), "no", "no", True, count, client_ip, client_port)
                    clients.append((client_ip, client_port))
                    seated_players.append(player)
                    print(count)
                    if(count>=2):
                        server_socket.settimeout(10)
                else:
                    response = "err"

                client_socket.send(response.encode('utf-8'))

            except socket.timeout:
                timeout = True
                server_socket.close()

            finally:
                try:
                    # Close the connection
                    if client_socket:
                        client_socket.close()
                except:
                    print("Exception")

        if count >= 2:
            print("Starting the game...")
            global game_phase
            socket_game = f"{server_host};888"
            for client_ip, client_port in clients:
                print(f"ip: {client_ip}; port: {client_port}")
                try:
                    # Create a socket for connecting to the player
                    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    player_socket.connect((client_ip, client_port))
                    player_socket.send(socket_game.encode('utf-8'))
                    player_socket.close()
                except Exception as e:
                    print(f"Error connecting to the player: {e}")

            # Crea un oggetto Thread
            
            thread_partita = threading.Thread(target=game, args=(game_phase, seated_players, winner_index))

            # thread = threading.Thread(target=partita)

            # Start the thread
            thread_partita.start()
            # thread_waiting.start()

            # Wait for the thread to finish before exiting
            thread_partita.join()
            # thread_waiting.join()
            print("Fake")
            clients=[]
            timeout = False
            count = 0

if __name__ == '__main__':
    main()
