class Player:
    """
    Represents a player in the poker game.

    Attributes:
        nome (str): The name of the player.
        carta1 (str): The first card of the player.
        carta2 (str): The second card of the player.
        puntata (int): The amount of chips the player has bet.
        soldi (int): The amount of chips the player has.
        turno (bool): Indicates if it's the player's turn.
        blind (bool): Indicates if the player is a blind.
        seduto (bool): Indicates if the player is seated.
        posto (int): The position of the player at the table.
        ip (str): The IP address of the player.
        port (int): The port number of the player's connection.
    """

    def __init__(self, nome, carta1, carta2, puntata, soldi, turno, blind, seduto, posto, ip, port):
        """
        Initializes a Player object with the given attributes.

        Args:
            nome (str): The name of the player.
            carta1 (str): The first card of the player.
            carta2 (str): The second card of the player.
            puntata (int): The amount of chips the player has bet.
            soldi (int): The amount of chips the player has.
            turno (bool): Indicates if it's the player's turn.
            blind (bool): Indicates if the player is a blind.
            seduto (bool): Indicates if the player is seated.
            posto (int): The position of the player at the table.
            ip (str): The IP address of the player.
            port (int): The port number of the player's connection.
        """
        self.nome = nome
        self.carta1 = carta1
        self.carta2 = carta2
        self.puntata = puntata
        self.soldi = soldi
        self.turno = turno
        self.blind = blind        
        self.seduto = seduto  
        self.posto = posto
        self.ip = ip
        self.port = port

    
