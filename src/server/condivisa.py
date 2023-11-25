seated_players=[]
game_phase=""
winner_index=0
count_player=0
server_socket=None
def set_info( _seated_palyer, _game_phase, _winner_index, _count_player, _server_socket):
    global seated_players
    global game_phase
    global winner_index
    global count_player
    global server_socket
    server_socket=_server_socket
    seated_players=_seated_palyer
    game_phase=_game_phase
    winner_index=_winner_index
    count_player=_count_player