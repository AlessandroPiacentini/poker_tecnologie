import socket

class Giocatore:
    # Costruttore della classe
    def __init__(self, nome, carte, puntata, soldi, turno, blind, seduto, posto, socket):
        self.nome = nome
        self.carte = carte
        self.puntata = puntata
        self.soldi = soldi
        self.turno = turno
        self.blind = blind        
        self.seduto = seduto  
        self.posto=posto
        self.socket=socket
        
        
    
    # def ciao(self):
    #     print("ciao")

    
