from main import game_phase, lock, seated_players, count
from Player import Player
import socket
import threading

# Initialize the vector for messages
seated_players = []
max_messages = 6

# Function that handles a client connection
def handle_client(client_socket, address, client_ip, client_port):
    global seated_players

    print(f"Connection accepted from {address}")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # If the client closes the connection, exit the loop

        # Check if the vector exceeds the maximum length
        if len(seated_players) >= max_messages:
            response = "table full"
            client_socket.send(response.encode("utf-8"))
            print(response)
            break
        else:
            # Decode and save the message in the vector
            message = data.decode("utf-8")
            player = Player(message.split(";")[1], 0, 0, 0, int(message.split(";")[2]), "no", "no", True, count, client_ip, client_port)
            seated_players.append(player)

        print(f"Received message: {message}")

    # Close the connection with the client
    client_socket.close()
    print(f"Connection closed with {address}")

def waiting():
    # Configure the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)

    print("Server listening on 127.0.0.1:12345")

    # Accept connections from clients
    while game_phase == "game":
        client_socket, client_address = server.accept()
        client_ip, client_port = client_address

        handle_client(client_socket, client_address, client_ip, client_port)
