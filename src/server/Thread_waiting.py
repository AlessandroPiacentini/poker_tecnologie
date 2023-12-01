from condivisa import SingletonClass
from Player import Player
import socket
import threading

singleton = SingletonClass()

# Function that handles a client connection
def handle_client(client_socket, address, client_ip, client_port):
    """
    Handle the client connection.

    Args:
        client_socket (socket): The socket object representing the client connection.
        address (tuple): The address of the client (IP address, port number).
        client_ip (str): The IP address of the client.
        client_port (int): The port number of the client.

    Returns:
        None
    """
    max_messages=6
    print(f"Connection accepted from {address}")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # If the client closes the connection, exit the loop

        # Check if the vector exceeds the maximum length
        if len(singleton.seated_players) >= max_messages:
            response = "table full"
            client_socket.send(response.encode("utf-8"))
            print(response)
            break
        else:
            # Decode and save the message in the vector
            message = data.decode("utf-8")
            singleton.count_player+=1
            player = Player(message.split(";")[1], 0, 0, 0, int(message.split(";")[2]), "no", "no", True, singleton.count_player, client_ip, client_port)
            singleton.seated_players.append(player)

        print(f"Received message: {message}")

    # Close the connection with the client
    client_socket.close()
    print(f"Connection closed with {address}")

def waiting():
    """
    Function that configures the server and waits for connections from clients.

    Args:
        None

    Returns:
        None
    """
    # Configure the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)
    
    

    print("Server listening on 127.0.0.1:12345")

    # Accept connections from clients
    while singleton.game_phase == "game":
        client_socket, client_address = server.accept()
        client_ip, client_port = client_address

        handle_client(client_socket, client_address, client_ip, client_port)
