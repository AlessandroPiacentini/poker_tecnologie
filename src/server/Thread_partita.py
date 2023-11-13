import socket
from Giocatore import Giocatore
import sqlite3


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

# Esempio di utilizzo della funzione
nome_database = "db/giocatori_seduti_tavolo.db"  # Sostituisci con il nome effettivo del tuo database
nome_tabella = "giocatori"  # Sostituisci con il nome effettivo della tua tabella
risultato_query = leggi_tabella_sqlite(nome_database, nome_tabella)

# Stampa il risultato senza l'indice
for riga in risultato_query:
    print(riga[1:])
svuota_tabella(nome_database, nome_tabella)


# def partita(fase_di_gioco):
#     risultato_query = leggi_tabella_sqlite(nome_database, nome_tabella)

#     # Stampa il risultato
#     giocatori_seduti_al_tavolo=[]
#     cout_turno=1
#     for riga in risultato_query:
#         g=Giocatore(riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11])
#         cout_turno+=1
#         giocatori_seduti_al_tavolo.append(g)
#     carte_uscite=[]
    
#     while fase_di_gioco=="game":

#         fase_di_gioco="waiting"