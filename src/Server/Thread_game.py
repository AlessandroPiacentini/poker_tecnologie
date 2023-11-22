import socket
from Player import Player  
import sqlite3
import xml.etree.ElementTree as ET

import threading
# from main import game_phase, lock, seated_players, winner_index

import random

#Estrae una carta da un mazzo di 52 carte, garantendo che ogni carta estratta non sia stata già utilizzata precedentemente.
def draw_card():
    global used_cards
    remake = True
    while remake:
        card = random.randint(1, 52)

        if card not in used_cards:
            remake = False

    return card                 #Ritorna il numero della carta da assegnare

#Creazione xml
def dict_to_xml(variables):
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

#Invia le informazioni ai giocatori
def send_info(players, pot, board_cards, game_phase_count):
    for player in players:
        try:
            # Crea un socket per la connessione al giocatore
            player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connessione a {player.ip}")
            player_socket.connect((player.ip, player.port))
            my_variables = {"pot": pot, "board_cards": board_cards, "game_phase_count": game_phase_count,
                            "players": players}

            xml_result = dict_to_xml(my_variables)
            che_cose = "dati"
            
            player_socket.send(che_cose.encode('utf-8'))
            player_socket.send(xml_result.encode('utf-8'))
            player_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")

#Small blind e big blind
def set_blind(turn, players):
    i = 0
    for player in players:
        if player.turn == turn + 1:
            players[i].blind = "small"
            players[i].bet = 5
        if player.turn == turn + 2:
            players[i].blind = "big"
            players[i].bet = 10

    return players

#Calcola il valore del tavolo
def calculate_pot(players):
    pot = 0
    for player in players:
        pot += player.bet
    return pot

#Riceve dal client la mossa eseguita
def receive_move():
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

#Distribuisce le carte ai giocatori seduti nel gioco.
def deal_player_cards():
    global seated_players
    i = 0
    while i < 2:
        for player in seated_players:
            if i == 0:
                player.card1 = draw_card()
            else:
                player.card2 = draw_card()
        i += 1

#Distribuisce le carte al tavolo
def deal_community_cards():
    i = 0
    while i < 3:
        community_cards.append(draw_card())
        i += 1

#Controlla se le puntate dei giocatori seduti sono tutte uguali.
def check_equal_bets():
    sentinel = True
    for player in seated_players:
        if player.seated:
            for player2 in seated_players:
                if player2.seated:
                    if player.bet != player2.bet:
                        sentinel = False
                        break
    return sentinel

#Calcola la puntata massima tra i giocatori attualmente seduti in una partita.
def calculate_max_bet():
    max_bet = 0
    for player in seated_players:
        if player.bet > max_bet:
            max_bet = player.bet
    return max_bet

#Resetta la puntata di tutti i giocatori
def reset_bets():
    for player in seated_players:
        player.bet = 0

#Valori delle carte combinate
def get_rank(card):
    # Funzione per ottenere il valore della carta per il ranking
    return (card - 1) % 13 + 1

def is_flush(hand):
    # Verifica se tutte le carte nella mano hanno lo stesso seme
    return len(set(card // 13 for card in hand)) == 1

def is_straight(hand):
    # Verifica se le carte nella mano formano una scala
    sorted_hand = sorted(get_rank(card) for card in hand)
    return sorted_hand[-1] - sorted_hand[0] == 4 and len(set(sorted_hand)) == 5

def evaluate_hand(hand, board):
    # Valutazione della mano sommando il valore delle carte
    return sum(get_rank(card) for card in hand + board)

#trova il vincitore
def find_winner():
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

# comunica il vincitore
def communicate_winner():
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

#E il run del thread
def game(game_phase_s, seated_players_s, winner_index_s):
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
            if len(seated_players) > 3:                                     #Se il numero di giocatori seduti è maggiore di 3 Imposta il BLIND
                seated_players = set_blind(turn_count, seated_players)
            if game_phase_count == 0:
                deal_player_cards()                                         #Distribuisce le carte ai giocatori seduti nel gioco.
            elif game_phase_count == 1:
                deal_community_cards()                                      #Distribuisce le carte al tavolo
            else:
                community_cards.append(draw_card())                         #Al terzo turno inizia a pescare
            
            #seated_players = array di giocatori con su le info
            send_info(seated_players, pot, community_cards, used_cards, game_phase_count)       #Invia i cambiamenti fatti nel server al Client

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
