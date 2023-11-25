


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
    
    
    
    

