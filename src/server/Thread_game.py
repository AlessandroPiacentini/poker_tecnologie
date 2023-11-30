import socket
from Player import Player  
import sqlite3
import xml.etree.ElementTree as ET

import threading
from condivisa import SingletonClass

import random


import time


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
    
    print(xml_string)
    
    return xml_string
def write_to_file(file_path, content):
    """
    Write content to a text file.

    Args:
        file_path (str): The path of the file to write to.
        content (str): The content to write to the file.

    Returns:
        None
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print("File written successfully.")
    except Exception as e:
        print(f"Error writing to file: {e}")

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
            
            
           
            my_variables = {"pot": pot, "board_cards": board_cards, "game_phase_count": game_phase_count,
                            "players": players, "turn": turn_count}
            print(pot)
            xml_result = dict_to_xml(my_variables)
            print("fatto xml")
            player.client_socket.send(xml_result.encode('utf-8'))
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
        player.bet = 0
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
    global singleton
    print(f"In attesa di connessioni su {server_host}:{server_port}...")
    

    time.sleep(1)
    # Ricevi i dati dal client
    data = singleton.seated_players[turn_count].client_socket.recv(1024)
    time.sleep(1)
    data_str = data.decode('utf-8')
    print(f"Dati ricevuti dal client: {data_str}")

    

    return data_str

def deal_player_cards():
    """
    Deals two cards to each player in the seated_players list.
    """
    global singleton
    for player in singleton.seated_players:
        i = 0
        while i < 2:
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
    global community_cards

    while i < 3:
        community_cards.append(draw_card())
        i += 1

def check_equal_bets():
    """
    Check if all seated players have equal bets.

    Returns:
        bool: True if all seated players have equal bets, False otherwise.
    """
    global singleton
    sentinel = True
    for player in singleton.seated_players:
        if player.seated:
            for player2 in singleton.seated_players:
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
    global singleton
    max_bet = 0
    for player in singleton.seated_players:
        if player.bet > max_bet:
            max_bet = player.bet
    return max_bet

def reset_bets():
    """
    Resets the bets of all seated players to zero.
    """
    global singleton
    for player in singleton.seated_players:
        player.bet = 0


from collections import Counter

def valuta_mano(mano):
    # Funzione per valutare la forza della mano
    valori = [carta[:-1] for carta in mano]
    count_valori = Counter(valori)

    # Verifica se ci sono coppie, tris, ecc.
    coppie = [valore for valore, count in count_valori.items() if count == 2]
    tris = [valore for valore, count in count_valori.items() if count == 3]
    poker = [valore for valore, count in count_valori.items() if count == 4]

    # Verifica se la mano contiene una scala
    valori_ordinati = sorted([int(valore) if valore.isdigit() else 11 if valore == 'J' else 12 if valore == 'Q' else 13 if valore == 'K' else 14 for valore in valori])
    scala = all(valori_ordinati[i] == valori_ordinati[i - 1] + 1 for i in range(1, len(valori_ordinati)))

    # Verifica se la mano contiene un colore
    semi = set(carta[-1] for carta in mano)
    colore = len(semi) == 1

    # Assegna un punteggio alla mano
    if scala and colore:
        return 9  # Scala reale
    elif poker:
        return 8  # Poker
    elif tris and coppie:
        return 7  # Full
    elif colore:
        return 6  # Colore
    elif scala:
        return 5  # Scala
    elif tris:
        return 4  # Tris
    elif coppie and len(coppie) == 2:
        return 3  # Due coppie
    elif coppie:
        return 2  # Coppia
    else:
        return 1  # Carta alta


def converti_mano(carta1, carta2):
    # Funzione per convertire le carte in stringhe
    carta1_str = str(carta1)
    carta2_str = str(carta2)

    if carta1_str[-1] == '1':
        carta1_str ='A'
    elif carta1_str[-1] == '11':
        carta1_str ='J'
    elif carta1_str[-1] == '12':
        carta1_str ='Q'
    elif carta1_str[-1] == '13':
        carta1_str ='K'

    if carta2_str[-1] == '1':
        carta2_str = 'A'
    elif carta2_str[-1] == '11':
        carta2_str = 'J'
    elif carta2_str[-1] == '12':
        carta2_str = 'Q'
    elif carta2_str[-1] == '13':
        carta2_str = 'K'


    if int(carta1/13)==1:
        carta1_str += 'D'
    elif int(carta1/13)==2:
        carta1_str += 'C'
    elif int(carta1/13)==3:
        carta1_str += 'H'
    elif int(carta1/13)==4:
        carta1_str += 'S'
        
        
    if int(carta2/13)==1:
        carta2_str += 'D'   
    elif int(carta2/13)==2:
        carta2_str += 'C'
    elif int(carta2/13)==3:
        carta2_str += 'H'
    elif int(carta2/13)==4:
        carta2_str += 'S'
        
        

    return [carta1_str, carta2_str]
def converti_board_card(carte):
    carte_convertite = []
    for carta in carte:
        carta_str = str(carta)
        if carta_str[-1] == '1':
            carta_str = 'A'
        elif carta_str[-1] == '11':
            carta_str = 'J'
        elif carta_str[-1] == '12':
            carta_str = 'Q'
        elif carta_str[-1] == '13':
            carta_str = 'K'

        if int(carta/13) == 1:
            carta_str += 'D'
        elif int(carta/13) == 2:
            carta_str += 'C'
        elif int(carta/13) == 3:
            carta_str += 'H'
        elif int(carta/13) == 4:
            carta_str += 'S'

        carte_convertite.append(carta_str)

    return carte_convertite


def determina_vincitore():
    # Funzione per determinare il vincitore tra i giocatori
    vincitore = None
    punteggio_vincitore = 0
    carte_comuni = converti_board_card(community_cards)
    for giocatore in singleton.seated_players:
        mano_completa = converti_mano(giocatore.card1, giocatore.card2) + carte_comuni
        punteggio_mano = valuta_mano(mano_completa)
        mano=converti_mano(giocatore.card1, giocatore.card2)

        if punteggio_mano > punteggio_vincitore or (punteggio_mano == punteggio_vincitore and valuta_carta_alta(mano) > valuta_carta_alta(converti_mano(vincitore.card1, vincitore.card2))):
            vincitore = giocatore
            punteggio_vincitore = punteggio_mano

    return vincitore.position

def valuta_carta_alta(mano):
    # Funzione per valutare la carta più alta in una mano
    valori = [carta[:-1] for carta in mano]
    valori_numerici = [int(valore) if valore.isdigit() else 11 if valore == 'J' else 12 if valore == 'Q' else 13 if valore == 'K' else 14 for valore in valori]
    return max(valori_numerici)

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
    global singleton
    for player in singleton.seated_players:
        try:
            # Crea un socket per la connessione al giocatore
            
            print(f"Connessione a {player.ip}")
            
            winner_index_str = str(winner_index)
            player.client_socket.send(winner_index_str.encode('utf-8'))
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")
            
def send_all_winner():
    global singleton
    for player in singleton.seated_players:
        try:
            # Crea un socket per la connessione al giocatore
            winner_str=str(singleton.winner_index)
            player.client_socket.send(winner_str.encode('utf-8'))
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")


def cout_player_alive():
    global singleton
    count=0
    for player in singleton.seated_players:
        if player.seated:
            count+=1
    return count       

singleton = SingletonClass()
used_cards=[]
pot=0
community_cards=[]
def game():
    """
    Main game loop that manages the flow of the poker game.

    Args:
        game_phase_s (str): The current game phase.
        seated_players_s (list): List of seated players.
        winner_index_s (int): Index of the winner.

    Returns:
        None
    """
    
    global turn_count
    turn_count = 0
    global community_cards
    global pot
    game_phase_count = 0
    global used_cards
    equal_bets = True
    global singleton
    deal_card=True
    deal_first3=True
    deal_card4=True
    deal_card5=True
    print(singleton.game_phase)
    while singleton.game_phase == "game":
        if singleton.seated_players[turn_count].seated and equal_bets:
            if len(singleton.seated_players) > 3:
                singleton.seated_players = set_blind(turn_count, singleton.seated_players)
            if game_phase_count==0 and deal_card:
                deal_player_cards()
                deal_card=False
                # deal_card=False
            elif game_phase_count == 1 and deal_first3:
                deal_community_cards()
                deal_first3=False
            elif game_phase_count == 2 and deal_card4:
                community_cards.append(draw_card())
                deal_card4=False
            elif game_phase_count == 3 and deal_card5:
                community_cards.append(draw_card())
                deal_card5=False
                

            send_info(singleton.seated_players, pot, community_cards, game_phase_count)

            move = receive_move()
            if move.split(";")[0] == "add":
                singleton.seated_players[turn_count].chips -= int( move.split(";")[1])
                singleton.seated_players[turn_count].bet = int( move.split(";")[1])
            elif move.split(";")[0] == "see":
                singleton.seated_players[turn_count].chips -= calculate_max_bet()
                singleton.seated_players[turn_count].bet = calculate_max_bet()
                
            elif move.split(";")[0] == "fold":
                singleton.seated_players[turn_count].seated = False
                if(cout_player_alive()==1):
                    singleton.game_phase="waiting"
                    break
                

        turn_count += 1
        if turn_count == len(singleton.seated_players):
            turn_count = 0
            if check_equal_bets():
                equal_bets = True
                game_phase_count += 1
                pot = calculate_pot(singleton.seated_players)
                reset_bets()
            else:
                equal_bets = False

        if game_phase_count > 3:
            singleton.game_phase = "waiting"
    singleton.winner_index = determina_vincitore()
    send_all_winner()
    singleton.server_socket.close()
    
