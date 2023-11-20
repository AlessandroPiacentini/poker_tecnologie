import socket
from Giocatore import Giocatore
import sqlite3
import xml.etree.ElementTree as ET

import threading
from main import fase_di_gioco, lock, giocatori_seduti, index_vincitore

import random




def svuota_tabella(nome_database, nome_tabella):
    connessione = sqlite3.connect(nome_database)
    cursore = connessione.cursor()

    # Esempio di query per svuotare la tabella
    query = f"DELETE FROM {nome_tabella}"
    cursore.execute(query)

    # Conferma i cambiamenti nel database
    connessione.commit()

    # Chiudi la connessione al database
    connessione.close()




def leggi_tabella_sqlite(nome_database, nome_tabella):
    connessione = sqlite3.connect(nome_database)
    cursore = connessione.cursor()

    # Esempio di query per selezionare tutti i record dalla tabella
    query = f"SELECT * FROM {nome_tabella}"
    cursore.execute(query)

    # Recupera tutti i record come una lista di tuple
    risultato = cursore.fetchall()

    # Chiudi la connessione al database
    connessione.close()

    return risultato

def pesca_carta():
    global carte_uscite
    remake=True
    while remake:
        carta= random.randint(1, 52)
    
        if carta not in carte_uscite:
            remake=False
            
    return carta




def dict_to_xml(variables):
    root = ET.Element("root")  # Sostituisci "root" con il nome desiderato per l'elemento radice

    for key, value in variables.items():
        element = ET.SubElement(root, key)
        if isinstance(value, list):
            # Se il valore è una lista, iteriamo sugli elementi della lista
            for item in value:
                if isinstance(item, Giocatore):
                    sub_element = ET.SubElement(element, "Giocatore")
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



def invio_info(giocatori_seduti, piatto, carte_banco, cout_fasi_partita):
    for giocatore in giocatori_seduti:
        try:
            # Crea un socket per la connessione al giocatore
            giocatore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"connessione a {giocatore.ip}")
            giocatore_socket.connect((giocatore.ip, giocatore.port))
            my_variables = {"piatto": piatto, "carte_banco": carte_banco,"cout_fasi_partita":cout_fasi_partita, "giocatori_seduti": giocatori_seduti}

            xml_result = dict_to_xml(my_variables)      
            giocatore_socket.send(xml_result.encode('utf-8'))
            giocatore_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")

def set_blind(turno, giocatori_seduti):
    i=0
    for giocatore in giocatori_seduti:
        if giocatore.turno==turno+1:
            giocatori_seduti[i].blind="small"
            giocatori_seduti[i].puntata=5
        if giocatore.turno==turno+2:
            giocatori_seduti[i].blind="big"
            giocatori_seduti[i].puntata=10
            
    return giocatori_seduti

def calcola_piatto(giocatori_seduti) :
    piatto=0
    for giocatore in giocatori_seduti:
        piatto+= giocatore.puntata
    return piatto 
  
  
def ricevi_mossa():
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


def dai_carte_giocatori():
    global giocatori_seduti
    i=0
    while i<2:
        for giocatore in giocatori_seduti:
            if i==0:
                giocatore.carta1=pesca_carta()
            else:
                giocatore.carta2=pesca_carta()
        i+=1
def prime_carte_banco():
    i=0
    while i<3:
        carte_banco.append(pesca_carta())
        i+=1 

def controllo_puntate_uguali():
    sentinella=True
    for giocatore in giocatori_seduti:
        if giocatore.seduto: 
            for giocatore2 in giocatori_seduti:
                if giocatore2.seduto: 
                    if giocatore.puntata!=giocatore2.puntata:
                        sentinella=False
                        break
    return sentinella


def calcola_max_puntata():
    max_puntata=0
    for giocatore in giocatori_seduti:
        if giocatore.puntata>max_puntata:
            max_puntata=giocatore.puntata
    return max_puntata

def azzera_puntate():
    for giocatore in giocatori_seduti:
        giocatore.puntata=0
 
 
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

def find_winner():
    global piatto
    # Trova il vincitore tra i giocatori in base alle carte in mano e le carte sul tavolo
    winner_index = 0
    best_score = evaluate_hand((giocatori_seduti[0].carta1, giocatori_seduti[0].carta2), carte_banco)

    for i in range(1, len(giocatori_seduti)):
        score = evaluate_hand((giocatori_seduti[i].carta1, giocatori_seduti[i].carta2), carte_banco)
        if score > best_score:
            winner_index = i
            best_score = score
    giocatori_seduti[winner_index+1].soldi+=piatto
    return winner_index+1       

def comunica_vincitore():
    global index_vincitore
    for giocatore in giocatori_seduti:
        try:
            # Crea un socket per la connessione al giocatore
            giocatore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"connessione a {giocatore.ip}")
            giocatore_socket.connect((giocatore.ip, giocatore.port))
            
            index_vincitore_str = str(index_vincitore)      
            giocatore_socket.send(index_vincitore_str.encode('utf-8'))
            giocatore_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")
    

carte_uscite=[]
giocatori_seduti=[]
carte_banco=[]
piatto=0

def partita():

    global giocatori_seduti
    cout_turno=1
    global fase_di_gioco
    global carte_banco
    global piatto
    cout_fasi_partita=0
    global carte_uscite
    puntate_uguali=True
    global index_vincitore

    
    
    while fase_di_gioco=="game":
        if giocatori_seduti[cout_turno].seduto and puntate_uguali:
            if len(giocatori_seduti)>3:
                giocatori_seduti=set_blind(cout_turno, giocatori_seduti)
            if cout_fasi_partita==0:
                dai_carte_giocatori()
            elif cout_fasi_partita==1:
                prime_carte_banco()
            else:
                carte_banco.append(pesca_carta())
            
            
            invio_info(giocatori_seduti, piatto, carte_banco, carte_uscite, cout_fasi_partita)
            
        
            mossa=ricevi_mossa()
            if mossa.split(";")[0]=="busso":
                pass
            elif mossa.split(";")[0]=="add":
                giocatori_seduti[cout_turno].puntata=mossa.split(";")[1]
            elif mossa.split(";")[0]=="vedi":
                giocatori_seduti[cout_turno].puntata=calcola_max_puntata()
            elif mossa.split(";")[0]=="lascia":
                giocatori_seduti[cout_turno].seduto=False
            
            
            
            
        
        cout_turno+=1
        if cout_turno==len(giocatori_seduti):
            cout_turno=1
            if controllo_puntate_uguali():
                puntate_uguali=True
                cout_fasi_partita+=1
                piatto=calcola_piatto(giocatori_seduti)
                azzera_puntate()
            else:
                puntate_uguali=False
    
        if cout_fasi_partita==3:
            fase_di_gioco="waiting"
        
    
    index_vincitore= find_winner()
    




    
# # Esempio di utilizzo della funzione
# nome_database = "db/giocatori_seduti_tavolo.db"  # Sostituisci con il nome effettivo del tuo database
# nome_tabella = "giocatori"  # Sostituisci con il nome effettivo della tua tabella
# risultato_query = leggi_tabella_sqlite(nome_database, nome_tabella)

# # # Stampa il risultato senza l'indice
# # for riga in risultato_query:
# #     print(riga[1:])
# def prova():
#     pass

# # Esempio di utilizzo:
# risultato_query = leggi_tabella_sqlite(nome_database, nome_tabella)
# giocatori_seduti_al_tavolo = []
# for riga in risultato_query:
#     g = Giocatore(riga[1], riga[2], riga[3], riga[4], riga[5], riga[6], riga[7], riga[8], riga[9], riga[10], riga[11])
#     giocatori_seduti_al_tavolo.append(g)
# carte_uscite=[] #array di int 
# carte_banco=[]#array di int
# piatto=0
# my_variables = {"piatto": piatto, "carte_banco": carte_banco,"carte_uscite": carte_uscite, "giocatori_seduti": giocatori_seduti_al_tavolo}

# xml_result = dict_to_xml(my_variables)
# print(xml_result)