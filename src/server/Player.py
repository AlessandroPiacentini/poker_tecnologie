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

    def __init__(self, name, card1, card2, bet, chips, turn, blind, seated, position, ip, port):
        """
        Initializes a Player object with the given attributes.

        Args:
            name (str): The name of the player.
            card1 (str): The first card of the player.
            card2 (str): The second card of the player.
            bet (int): The amount of chips the player has bet.
            chips (int): The amount of chips the player has.
            turn (bool): Indicates if it's the player's turn.
            blind (bool): Indicates if the player is a blind.
            seated (bool): Indicates if the player is seated.
            position (int): The position of the player at the table.
            ip (str): The IP address of the player.
            port (int): The port number of the player's connection.
        """
        self.name = name
        self.card1 = card1
        self.card2 = card2
        self.bet = bet
        self.chips = chips
        self.turn = turn
        self.blind = blind        
        self.seated = seated  
        self.position = position
        self.ip = ip
        self.port = port


    
