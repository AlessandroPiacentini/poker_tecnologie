import socket
from Giocatore import Giocatore
import sqlite3
import xml.etree.ElementTree as ET



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



def invio_info(giocatori_seduti_al_tavolo, piatto, carte_banco, carte_uscite):
    for giocatore in giocatori_seduti_al_tavolo:
        try:
            # Crea un socket per la connessione al giocatore
            giocatore_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"connessione a {giocatore.ip}")
            giocatore_socket.connect((giocatore.ip, giocatore.port))
            my_variables = {"piatto": piatto, "carte_banco": carte_banco,"carte_uscite": carte_uscite, "giocatori_seduti": giocatori_seduti_al_tavolo}

            xml_result = dict_to_xml(my_variables)      
            giocatore_socket.send(xml_result.encode('utf-8'))
            giocatore_socket.close()
        except Exception as e:
            print(f"Errore durante la connessione al giocatore: {e}")


  
def partita(fase_di_gioco, giocatori_seduti):

    # Stampa il risultato
    giocatori_seduti_al_tavolo=giocatori_seduti
    cout_turno=1
    
    carte_uscite=[]
    carte_banco=[]
    piatto=0
    
    while fase_di_gioco=="game":
        if cout_turno==6:
            cout_turno=0
        invio_info(giocatori_seduti_al_tavolo, piatto, carte_banco, carte_uscite)
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

        cout_turno+=1
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