import socket
from Giocatore import Giocatore
import sqlite3
import xml.etree.ElementTree as ET

import threading
from main import fase_di_gioco, lock

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



def invio_info(giocatori_seduti_al_tavolo, piatto, carte_banco):
    for giocatore in giocatori_seduti_al_tavolo:
        try:
            # Crea un socket per la connessione al giocatore
            giocatore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"connessione a {giocatore.ip}")
            giocatore_socket.connect((giocatore.ip, giocatore.port))
            my_variables = {"piatto": piatto, "carte_banco": carte_banco, "giocatori_seduti": giocatori_seduti_al_tavolo}

            xml_result = dict_to_xml(my_variables)      
            giocatore_socket.send(xml_result.encode('utf-8'))
            giocatore_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")

def set_blind(turno, giocatori_seduti_al_tavolo):
    i=0
    for giocatore in giocatori_seduti_al_tavolo:
        if giocatore.turno==turno+1:
            giocatori_seduti_al_tavolo[i].blind="small"
            giocatori_seduti_al_tavolo[i].puntata=5
        if giocatore.turno==turno+2:
            giocatori_seduti_al_tavolo[i].blind="big"
            giocatori_seduti_al_tavolo[i].puntata=10
            
    return giocatori_seduti_al_tavolo

def calcola_piatto(giocatori_seduti_al_tavolo) :
    piatto=0
    for giocatore in giocatori_seduti_al_tavolo:
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
    global giocatori_seduti_al_tavolo
    i=0
    while i<2:
        for giocatore in giocatori_seduti_al_tavolo:
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
    for giocatore in giocatori_seduti_al_tavolo:
        if giocatore.seduto: 
            for giocatore2 in giocatori_seduti_al_tavolo:
                if giocatore2.seduto: 
                    if giocatore.puntata!=giocatore2.puntata:
                        sentinella=False
                        break
    return sentinella
carte_uscite=[]
giocatori_seduti_al_tavolo=[]
carte_banco=[]
def partita(giocatori_seduti):

    global giocatori_seduti_al_tavolo
    giocatori_seduti_al_tavolo=giocatori_seduti
    cout_turno=1
    global fase_di_gioco
    global carte_banco
    piatto=0
    cout_fasi_partita=0
    global carte_uscite
    puntate_uguali=True

    
    
    while fase_di_gioco=="game":
        
        if puntate_uguali:
            if len(giocatori_seduti_al_tavolo)>3:
                giocatori_seduti_al_tavolo=set_blind(cout_turno, giocatori_seduti_al_tavolo)
            if cout_fasi_partita==0:
                dai_carte_giocatori()
            elif cout_fasi_partita==1:
                prime_carte_banco()
            else:
                carte_banco.append(pesca_carta())
            
            piatto=calcola_piatto(giocatori_seduti_al_tavolo)
            invio_info(giocatori_seduti_al_tavolo, piatto, carte_banco, carte_uscite)
            
        
        mossa=ricevi_mossa()
        if mossa.split(";")[0]=="busso":
            pass
        elif mossa.split(";")[0]=="add":
            giocatori_seduti_al_tavolo[cout_turno].puntata=mossa.split(";")[1]
            invio_info(giocatori_seduti_al_tavolo, piatto, carte_banco)
        
        
        
        
        cout_turno+=1
        if cout_turno==len(giocatori_seduti_al_tavolo):
            cout_turno=1
        if controllo_puntate_uguali():
            puntate_uguali=True
            cout_fasi_partita+=1
        else:
            puntate_uguali=False
    
        if cout_fasi_partita==3:
            fase_di_gioco="waiting"
        
    giocatori_seduti_al_tavolo=[]
    


    
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