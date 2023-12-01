


class SingletonClass(object):
  """
  A class that implements the Singleton design pattern.

  This class ensures that only one instance of the class is created and provides a global point of access to it.

  Attributes:
    instance: The single instance of the class.

  Methods:
    __new__(cls): Creates a new instance of the class if it doesn't exist, otherwise returns the existing instance.
  """

  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance


singleton = SingletonClass()

singleton.seated_players = []
singleton.game_phase = ""
singleton.winner_index = 0
singleton.count_player = 0
singleton.server_socket = None


def set_info(_seated_player, _game_phase, _winner_index, _count_player, _server_socket):
  """
  Sets the information in the Singleton instance.

  Args:
    _seated_player: A list of seated players.
    _game_phase: The current game phase.
    _winner_index: The index of the winner player.
    _count_player: The count of players.
    _server_socket: The server socket.

  Returns:
    None
  """
  singleton = SingletonClass()
  singleton.server_socket = _server_socket
  singleton.seated_players = _seated_player
  singleton.game_phase = _game_phase
  singleton.winner_index = _winner_index
  singleton.count_player = _count_player
class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance
   


singleton = SingletonClass()

singleton.seated_players=[]
singleton.game_phase=""
singleton.winner_index=0
singleton.count_player=0
singleton.server_socket=None


def set_info( _seated_palyer, _game_phase, _winner_index, _count_player, _server_socket):
    singleton = SingletonClass()
    singleton.server_socket=_server_socket
    singleton.seated_players=_seated_palyer
    singleton.game_phase=_game_phase
    singleton.winner_index=_winner_index
    singleton.count_player=_count_player
    
    
    
    

