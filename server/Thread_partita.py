import socket
from Giocatore import Giocatore

def partita(giocatori_seduti, fase_di_gioco):
    while fase_di_gioco=="game":
        print("partita finita")
        fase_di_gioco="waiting"