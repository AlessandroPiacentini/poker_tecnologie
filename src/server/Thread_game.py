import socket
from Player import Player  
import sqlite3
import xml.etree.ElementTree as ET

import threading
# from main import game_phase, lock, seated_players, winner_index

import random

def draw_card():
    """
    Function to draw a card from a deck of cards.

    Returns:
        int: The number representing the drawn card.
    """
    global used_cards
    remake = True
    while remake:
        card = random.randint(1, 52)

        if card not in used_cards:
            remake = False

    return card

def dict_to_xml(variables):
    """
    Convert a dictionary to an XML string.

    Args:
        variables (dict): The dictionary to be converted.

    Returns:
        str: The XML string representation of the dictionary.
    """
    root = ET.Element("root") 
    for key, value in variables.items():
        element = ET.SubElement(root, key)
        if isinstance(value, list):
            # Se il valore è una lista, itera sugli elementi della lista
            for item in value:
                if isinstance(item, Player):
                    sub_element = ET.SubElement(element, "Player")
                    for attrib_name, attrib_value in item.__dict__.items():
                        attrib_element = ET.SubElement(sub_element, attrib_name)
                        attrib_element.text = str(attrib_value)
                elif isinstance(item, int):
                    item_element = ET.SubElement(element, "item")
                    item_element.text = str(item)
        else:
            element.text = str(value)

    xml_string = ET.tostring(root).decode("utf-8")
    return xml_string

def send_info(players, pot, board_cards, game_phase_count):
    """
    Sends game information to each player.

    Args:
        players (list): List of Player objects representing the players in the game.
        pot (int): The current pot amount.
        board_cards (list): List of cards on the board.
        game_phase_count (int): The current game phase count.

    Returns:
        None
    """
    for player in players:
        try:
            # Crea un socket per la connessione al giocatore
            player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connessione a {player.ip}")
            player_socket.connect((player.ip, player.port))
            my_variables = {"pot": pot, "board_cards": board_cards, "game_phase_count": game_phase_count,
                            "players": players}

            xml_result = dict_to_xml(my_variables)
            player_socket.send(xml_result.encode('utf-8'))
            player_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")

def set_blind(turn, players):
    """
    Sets the blind and bet for the players based on the turn.

    Parameters:
    turn (int): The current turn.
    players (list): The list of players.

    Returns:
    list: The updated list of players with the blind and bet set.
    """
    i = 0
    for player in players:
        if player.turn == turn + 1:
            players[i].blind = "small"
            players[i].bet = 5
        if player.turn == turn + 2:
            players[i].blind = "big"
            players[i].bet = 10

    return players

def calculate_pot(players):
    """
    Calculate the total pot amount based on the bets of all players.

    Args:
        players (list): A list of Player objects representing the players in the game.

    Returns:
        int: The total pot amount.
    """
    pot = 0
    for player in players:
        pot += player.bet
    return pot

def receive_move():
    """
    Receive move from the client.

    Returns:
        str: The move received from the client.
    """
    server_host = '127.0.0.1'
    server_port = 888
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(6)
    server_socket.settimeout(15)
    print(f"In attesa di connessioni su {server_host}:{server_port}...")
    client_socket, client_address = server_socket.accept()
    client_ip, client_port = client_address  # Estrai l'indirizzo IP e la porta

    print(f"Connessione da: {client_address}")

    # Ricevi i dati dal client
    data = client_socket.recv(1024)
    data_str = data.decode('utf-8')
    print(f"Dati ricevuti dal client: {data_str}")

    # Decodifica i dati da bytes a stringa
    response = f"ok"
    client_socket.send(response.encode('utf-8'))
    server_socket.close()

    return data_str

def deal_player_cards():
    """
    Deals two cards to each player in the seated_players list.
    """
    global seated_players
    i = 0
    while i < 2:
        for player in seated_players:
            if i == 0:
                player.card1 = draw_card()
            else:
                player.card2 = draw_card()
        i += 1

def deal_community_cards():
    """
    Deals three community cards by appending them to the `community_cards` list.
    """
    i = 0
    while i < 3:
        community_cards.append(draw_card())
        i += 1

def check_equal_bets():
    """
    Check if all seated players have equal bets.

    Returns:
        bool: True if all seated players have equal bets, False otherwise.
    """
    sentinel = True
    for player in seated_players:
        if player.seated:
            for player2 in seated_players:
                if player2.seated:
                    if player.bet != player2.bet:
                        sentinel = False
                        break
    return sentinel

def calculate_max_bet():
    """
    Calculate the maximum bet among all seated players.

    Returns:
        int: The maximum bet value.
    """
    max_bet = 0
    for player in seated_players:
        if player.bet > max_bet:
            max_bet = player.bet
    return max_bet

def reset_bets():
    """
    Resets the bets of all seated players to zero.
    """
    for player in seated_players:
        player.bet = 0

def get_rank(card):
    """
    Get the rank value of a card for ranking purposes.

    Parameters:
    card (int): The numerical value of the card.

    Returns:
    int: The rank value of the card.
    """
    return (card - 1) % 13 + 1

def is_flush(hand):
    """
    Check if all cards in the hand have the same suit.

    Args:
        hand (list): A list of integers representing the cards in the hand.

    Returns:
        bool: True if all cards have the same suit, False otherwise.
    """
    return len(set(card // 13 for card in hand)) == 1

def is_straight(hand):
    """
    Check if the cards in the hand form a straight.

    Args:
        hand (list): A list of cards in the hand.

    Returns:
        bool: True if the hand forms a straight, False otherwise.
    """
    sorted_hand = sorted(get_rank(card) for card in hand)
    return sorted_hand[-1] - sorted_hand[0] == 4 and len(set(sorted_hand)) == 5

def evaluate_hand(hand, board):
    """
    Evaluate the strength of a poker hand by summing the values of the cards.

    Parameters:
    hand (list): A list of cards representing the player's hand.
    board (list): A list of cards representing the community cards on the board.

    Returns:
    int: The total value of the hand.

    """
    return sum(get_rank(card) for card in hand + board)

def find_winner():
    """
    Finds the winner among the players based on their hand cards and the community cards.

    Returns:
        int: The index of the winner player.
    """
    global pot
    # Trova il vincitore tra i giocatori in base alle carte in mano e le carte sul tavolo
    winner_index = 0
    best_score = evaluate_hand((seated_players[0].card1, seated_players[0].card2), community_cards)

    for i in range(1, len(seated_players)):
        score = evaluate_hand((seated_players[i].card1, seated_players[i].card2), community_cards)
        if score > best_score:
            winner_index = i
            best_score = score
    seated_players[winner_index + 1].chips += pot
    return winner_index + 1

def communicate_winner():
    """
    Communicates the winner index to each seated player.

    This function creates a socket connection to each player and sends the winner index.
    If an error occurs during the connection, it prints the error message.

    Parameters:
    None

    Returns:
    None
    """
    global winner_index
    for player in seated_players:
        try:
            # Crea un socket per la connessione al giocatore
            player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connessione a {player.ip}")
            player_socket.connect((player.ip, player.port))

            winner_index_str = str(winner_index)
            player_socket.send(winner_index_str.encode('utf-8'))
            player_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")

used_cards = []
seated_players = []
community_cards = []
pot = 0

def game(game_phase_s, seated_players_s, winner_index_s):
    """
    Main game loop that manages the flow of the poker game.

    Args:
        game_phase_s (str): The current game phase.
        seated_players_s (list): List of seated players.
        winner_index_s (int): Index of the winner.

    Returns:
        None
    """
    global seated_players
    seated_players=seated_players_s
    turn_count = 1
    global game_phase
    game_phase=game_phase_s
    global community_cards
    global pot
    game_phase_count = 0
    global used_cards
    equal_bets = True
    global winner_index
    winner_index=winner_index_s

    while game_phase == "game":
        if seated_players[turn_count].seated and equal_bets:
            if len(seated_players) > 3:
                seated_players = set_blind(turn_count, seated_players)
            if game_phase_count == 0:
                deal_player_cards()
            elif game_phase_count == 1:
                deal_community_cards()
            else:
                community_cards.append(draw_card())

            send_info(seated_players, pot, community_cards, used_cards, game_phase_count)

            move = receive_move()
            if move.split(";")[0] == "knock":
                pass
            elif move.split(";")[0] == "add":
                seated_players[turn_count].bet = move.split(";")[1]
            elif move.split(";")[0] == "see":
                seated_players[turn_count].bet = calculate_max_bet()
            elif move.split(";")[0] == "leave":
                seated_players[turn_count].seated = False

        turn_count += 1
        if turn_count == len(seated_players):
            turn_count = 1
            if check_equal_bets():
                equal_bets = True
                game_phase_count += 1
                pot = calculate_pot(seated_players)
                reset_bets()
            else:
                equal_bets = False

        if game_phase_count == 3:
            game_phase = "waiting"

    winner_index = find_winner()
