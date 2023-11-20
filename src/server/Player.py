import socket

class Player:
    # Costruttore della classe
    def __init__(self, nome, carta1, carta2, puntata, soldi, turno, blind, seduto, posto, ip, port):
        self.nome = nome
        self.carta1 = carta1
        self.carta2 = carta2
        self.puntata = puntata
        self.soldi = soldi
        self.turno = turno
        self.blind = blind        
        self.seduto = seduto  
        self.posto=posto
        self.ip=ip
        self.port=port
        
        
    
    # def ciao(self):
    #     print("ciao")

    
