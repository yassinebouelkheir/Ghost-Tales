import map
import random
import blessed
term = blessed.Terminal()

GAME_LINES = 20
GAME_COLUMNS = 20

MAX_GHOSTS = 100
MAX_MAGICS = 100

GAME_MODE_P_VS_P = 0
GAME_MODE_P_VS_AI = 1
GAME_MODE_AI_VS_AI = 2

PLAYER_1 = 0
PLAYER_2 = 1

PLAYER_STATS_COLUMNS_FACTOR = 8
PLAYER_STATS_LINES_FACTOR = 0.2

game_mode = -1
player_turn = 0
ghost = [{'playerid': -1, 'x':-1, 'y':-1, 'magicid': -1, 'points':0, 'icon': -1} for x in range(MAX_GHOSTS)]
magic = [{'x':-1, 'y':-1, 'type': -1, 'used': 0, 'points':0, 'icon': -1} for x in range(MAX_MAGICS)]

def get_pool_id(item_type):
    for i in range(0, 100):
        if item_type == map.ITEM_TYPE_GHOST:
            if ghost[i]['playerid'] == -1:
                return i
        elif item_type == map.ITEM_TYPE_MAGIC:
            if magic[i]['type'] == -1:
                return i    
        else:
            raise TypeError("[main.py:get_pool_id] Error 07: indefined item type (item_type: " + str(item_type) +")")     
    raise TypeError("[main.py:get_pool_id] Error 12: cannot generate new id, item array is full (item_type: " + str(item_type) +")")     

def ghost_set_position(ghostid, x, y, icon=-1):
    if ghostid > (MAX_GHOSTS-1) or ghostid < 0:
        raise TypeError("[main.py:ghost_set_position] Error 08: invalid ghostid (ghostid: " + str(ghostid) +")")
    if ghost[ghostid]['points'] < 1:
        raise TypeError("[main.py:ghost_set_position] Error 08: invalid ghostid (ghostid: " + str(ghostid) +")")
    if (ghost[ghostid]['x'] < 0 or ghost[ghostid]['x'] > (map.global_lines-1)) or (ghost[ghostid]['y'] < 0 or ghost[ghostid]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:ghost_set_position] Error 09: invalid ghost positions (ghostid: " + str(ghostid) +", x: " + str(x) +", y: " + str(y) +")")
    
    map.item_update(x, y, map.ITEM_DELETE)
    for i in magic:
        if magic[i]['x'] == x and magic[i]['y'] == y:
            collect_magic(ghostid, i)

    map.item_update(x, y, map.ITEM_ADD, map.ITEM_TYPE_GHOST, ghostid, ghost[ghostid]['playerid'], icon)
    ghost[ghostid]['x'] = x
    ghost[ghostid]['y'] = y
    ghost[ghostid]['icon'] = icon

def items_generate(item_type, number):
    if number > (map.global_lines*map.global_columns) or number < 0:
        raise TypeError("[main.py:item_generate] Error 11: number of items to generate is out of bounds (number: " + str(number) +")")
    if item_type == map.ITEM_TYPE_GHOST:
        for i in range(0, number):
            x, y = 0, 0
            k = 0
            while(k == 0):
                x = random.randint(0, map.global_lines-1)
                y = random.randint(0, map.global_columns-1)
                if(map.position_state[x][y] != 1):
                    k = 1
            playerid = (PLAYER_2 if i >= number/2 else PLAYER_1)
            ghostid = get_pool_id(map.ITEM_TYPE_GHOST)
            map.item_update(x, y, map.ITEM_ADD, map.ITEM_TYPE_GHOST, ghostid, playerid)
            ghost[ghostid]['playerid'] = playerid
            ghost[ghostid]['x'] = x
            ghost[ghostid]['y'] = y
            ghost[ghostid]['magicid'] = -1
            ghost[ghostid]['points'] = 100
            ghost[ghostid]['icon'] = -1

    elif item_type == map.ITEM_TYPE_MAGIC:
        for i in range(0, number):
            x, y = 0, 0
            k = 0
            while(k == 0):
                x = random.randint(0, map.global_lines-1)
                y = random.randint(0, map.global_columns-1)
                if(map.position_state[x][y] != 1):
                    k = 1
            magicid = get_pool_id(map.ITEM_TYPE_MAGIC)
            map.item_update(x, y, map.ITEM_ADD, map.ITEM_TYPE_MAGIC, magicid)
            magic[magicid]['x'] = x
            magic[magicid]['y'] = y
            magic[magicid]['type'] = 0
            magic[magicid]['used'] = 0
            magic[magicid]['points'] = 100
            magic[magicid]['icon'] = -1
    else:
        raise TypeError("[main.py:item_generate] Error 07: indefined item type (item_type: " + str(item_type) +")")

def terminal_read_command():
    global player_turn, game_mode
    if game_mode < 0 or game_mode > GAME_MODE_AI_VS_AI:
        raise TypeError("[main.py:terminal_read_command] Error 12: invalid gamemode (game_mode: " + str(game_mode) +")")
    while(1):
        if player_turn == PLAYER_1:
            if game_mode == GAME_MODE_P_VS_P or game_mode == GAME_MODE_P_VS_AI:
                command = input("Player's 1 turn, enter your command: ") 
                execute_command(player_turn, command)    
            elif game_mode == GAME_MODE_AI_VS_AI:
                player_turn = PLAYER_2
            player_turn = PLAYER_2
        elif player_turn == PLAYER_2:
            if game_mode == GAME_MODE_P_VS_P:
                command = input("Player's 2 turn, enter your command: ") 
                execute_command(player_turn, command)    
            elif game_mode == GAME_MODE_P_VS_AI:
                player_turn = PLAYER_1
            elif game_mode == GAME_MODE_AI_VS_AI:
                player_turn = PLAYER_1
            player_turn = PLAYER_1
        else:
            raise TypeError("[main.py:terminal_read_command] Error 10: invalid playerid (playerid: " + str(player_turn) +")")

def execute_command(playerid, cmd): # A FAIRE
    map.map_update(map.global_border_vertical)
    print_players_stats()
    return

def global_variables_reinit():
    global player_turn, ghost, magic
    player_turn = 0
    ghost = [{'playerid': -1, 'x':-1, 'y':-1, 'magicid': -1, 'points':0, 'icon': -1} for x in range(MAX_GHOSTS)]
    magic = [{'x':-1, 'y':-1, 'type': -1, 'used': 0, 'points':0, 'icon': -1} for x in range(MAX_MAGICS)]
    map.global_border_horizontal = ''
    map.global_border_vertical = ''
    map.global_lines = 0
    map.global_columns = 0
    map.positions = [[0 for x in range(map.MAX_POSITIONS)] for x in range(map.MAX_POSITIONS)]
    map.position_state = [[0 for x in range(map.MAX_POSITIONS)] for x in range(map.MAX_POSITIONS)]

def select_game_mode():
    global game_mode
    command = input("To start, choose a game mode (1v1/1vC/CvC): ") 
    if command == '1v1':
        game_mode = GAME_MODE_P_VS_P
    elif command == '1vC':
        game_mode = GAME_MODE_P_VS_AI
    elif command == 'CvC':
        game_mode = GAME_MODE_AI_VS_AI 
    else:
        select_game_mode()

def game_init(lines, columns, reinit=0):
    if reinit == 1:
        global_variables_reinit()
    map.build_empty_map(lines,columns)
    map.generate_positions_list(lines, columns)
    select_game_mode()
    items_generate(map.ITEM_TYPE_GHOST, int(MAX_GHOSTS/2))
    items_generate(map.ITEM_TYPE_MAGIC, int(MAX_MAGICS/4))
    print_players_stats()
    terminal_read_command()

def game_over(winnerid): # A FAIRE
    return

def attack_ghost(ghostid_victim, ghostid_killer): # A FAIRE
    if ghostid_victim > (MAX_GHOSTS-1) or ghostid_victim < 0:
        raise TypeError("[main.py:attack_ghost] Error 08: invalid ghostid (ghostid_victim: " + str(ghostid_victim) +")")
    if ghost[ghostid_victim]['points'] < 1:
        raise TypeError("[main.py:attack_ghost] Error 08: invalid ghostid (ghostid_victim: " + str(ghostid_victim) +")")
    if (ghost[ghostid_victim]['x'] < 0 or ghost[ghostid_victim]['x'] > (map.global_lines-1)) or (ghost[ghostid_victim]['y'] < 0 or ghost[ghostid_victim]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:attack_ghost] Error 09: invalid ghost positions (ghostid_victim: " + str(ghostid_victim) +", x: " + str(ghost[ghostid_victim]['x']) +", y: " + str(ghost[ghostid_victim]['y']) +")")
    
    if ghostid_killer > (MAX_GHOSTS-1) or ghostid_killer < 0:
        raise TypeError("[main.py:attack_ghost] Error 08: invalid ghostid (ghostid_killer: " + str(ghostid_killer) +")")
    if ghost[ghostid_killer]['points'] < 1:
        raise TypeError("[main.py:attack_ghost] Error 08: invalid ghostid (ghostid_killer: " + str(ghostid_killer) +")")
    if (ghost[ghostid_killer]['x'] < 0 or ghost[ghostid_killer]['x'] > (map.global_lines-1)) or (ghost[ghostid_killer]['y'] < 0 or ghost[ghostid_killer]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:attack_ghost] Error 09: invalid ghost positions (ghostid_killer: " + str(ghostid_killer) +", x: " + str(ghost[ghostid_killer]['x']) +", y: " + str(ghost[ghostid_killer]['y']) +")")


def kill_ghost(ghostid_victim, ghostid_killer):
    if ghostid_victim > (MAX_GHOSTS-1) or ghostid_victim < 0:
        raise TypeError("[main.py:kill_ghost] Error 08: invalid ghostid (ghostid_victim: " + str(ghostid_victim) +")")
    if ghost[ghostid_victim]['points'] < 1:
        raise TypeError("[main.py:kill_ghost] Error 08: invalid ghostid (ghostid_victim: " + str(ghostid_victim) +")")
    if (ghost[ghostid_victim]['x'] < 0 or ghost[ghostid_victim]['x'] > (map.global_lines-1)) or (ghost[ghostid_victim]['y'] < 0 or ghost[ghostid_victim]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:kill_ghost] Error 09: invalid ghost positions (ghostid_victim: " + str(ghostid_victim) +", x: " + str(ghost[ghostid_victim]['x']) +", y: " + str(ghost[ghostid_victim]['y']) +")")
    
    if ghostid_killer > (MAX_GHOSTS-1) or ghostid_killer < 0:
        raise TypeError("[main.py:kill_ghost] Error 08: invalid ghostid (ghostid_killer: " + str(ghostid_killer) +")")
    if ghost[ghostid_killer]['points'] < 1:
        raise TypeError("[main.py:kill_ghost] Error 08: invalid ghostid (ghostid_killer: " + str(ghostid_killer) +")")
    if (ghost[ghostid_killer]['x'] < 0 or ghost[ghostid_killer]['x'] > (map.global_lines-1)) or (ghost[ghostid_killer]['y'] < 0 or ghost[ghostid_killer]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:kill_ghost] Error 09: invalid ghost positions (ghostid_killer: " + str(ghostid_killer) +", x: " + str(ghost[ghostid_killer]['x']) +", y: " + str(ghost[ghostid_killer]['y']) +")")
    
    map.item_update(ghost[ghostid_victim]['x'], ghost[ghostid_victim]['y'], map.ITEM_DELETE)
    map.item_update(ghost[ghostid_killer]['x'], ghost[ghostid_killer]['y'], map.ITEM_DELETE)
    ghost[ghostid_killer]['x'] = ghost[ghostid_victim]['x']
    ghost[ghostid_killer]['y'] = ghost[ghostid_victim]['y']
    map.item_update(ghost[ghostid_killer]['x'], ghost[ghostid_killer]['y'], map.ITEM_ADD, map.ITEM_TYPE_GHOST, ghostid_killer, ghost[ghostid_killer]['playerid'])    

    ghost[ghostid_killer]['points'] += 100 # A CHANGER

    ghost[ghostid_victim]['x'] = -1
    ghost[ghostid_victim]['y'] = -1
    ghost[ghostid_victim]['magicid'] = -1
    ghost[ghostid_victim]['points'] = 0
    ghost[ghostid_victim]['icon'] = -1

    points, ghosts = get_player_stats(ghost[ghostid_victim]['playerid'])
    if points == 0 or ghosts == 0:
        game_over(ghost[ghostid_killer]['playerid'])

    ghost[ghostid_victim]['playerid'] = -1

def collect_magic(ghostid, magicid):
    if ghostid > (MAX_GHOSTS-1) or ghostid < 0:
        raise TypeError("[main.py:collect_magic] Error 08: invalid ghostid (ghostid: " + str(ghostid) +")")
    if ghost[ghostid]['points'] < 1:
        raise TypeError("[main.py:collect_magic] Error 08: invalid ghostid (ghostid: " + str(ghostid) +")")
    if (ghost[ghostid]['x'] < 0 or ghost[ghostid]['x'] > (map.global_lines-1)) or (ghost[ghostid]['y'] < 0 or ghost[ghostid]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:collect_magic] Error 09: invalid ghost positions (ghostid: " + str(ghostid) +", x: " + str(ghost[ghostid]['x']) +", y: " + str(ghost[ghostid]['y']) +")")
    
    if magicid > (MAX_MAGICS-1) or magicid < 0:
        raise TypeError("[main.py:collect_magic] Error 08: invalid magicid (magicid: " + str(magicid) +")")
    if magic[magicid]['points'] < 1:
        raise TypeError("[main.py:collect_magic] Error 08: invalid magicid (magicid: " + str(magicid) +")")
    if (magic[magicid]['x'] < 0 or magic[magicid]['x'] > (map.global_lines-1)) or (magic[magicid]['y'] < 0 or magic[magicid]['y'] > (map.global_columns-1)):
        raise TypeError("[main.py:collect_magic] Error 09: invalid magic positions (magicid: " + str(magicid) +", x: " + str(magic[magicid]['x']) +", y: " + str(magic[magicid]['y']) +")")
    
    map.item_update(ghost[ghostid]['x'], ghost[ghostid]['y'], map.ITEM_DELETE)
    map.item_update(magic[magicid]['x'], magic[magicid]['y'], map.ITEM_DELETE)
    ghost[ghostid]['x'] = magic[magicid]['x']
    ghost[ghostid]['y'] = magic[magicid]['y']
    map.item_update(ghost[ghostid]['x'], ghost[ghostid]['y'], map.ITEM_ADD, map.ITEM_TYPE_GHOST, ghostid, ghost[ghostid]['playerid'])    
    if ghost[ghostid]['magicid'] != -1:
        magic[ghost[ghostid]['magicid']]['x'] = -1
        magic[ghost[ghostid]['magicid']]['y'] = -1
        magic[ghost[ghostid]['magicid']]['type'] = -1
        magic[ghost[ghostid]['magicid']]['used'] = 0
        magic[ghost[ghostid]['magicid']]['points'] = 0
        magic[ghost[ghostid]['magicid']]['icon'] = -1

    magic[magicid]['x'] = -1
    magic[magicid]['y'] = -1
    magic[magicid]['used'] = 1
    ghost[ghostid]['magicid'] = magicid
    ghost[ghostid]['points'] += magic[magicid]['points']

def get_player_stats(playerid):
    if playerid > 1 or playerid < 0:
        raise TypeError("[main.py:get_player_stats] Error 10: invalid playerid (playerid: " + str(playerid) +")")
    points = 0
    ghosts = 0
    for i in range(0, MAX_GHOSTS):
        if ghost[i]['playerid'] == playerid:
            points += ghost[i]['points']
            ghosts += 1
    return points, ghosts

def print_players_stats():
    global game_mode
    if game_mode < 0 or game_mode > GAME_MODE_AI_VS_AI:
        raise TypeError("[main.py:print_player_stats] Error 12: invalid gamemode (game_mode: " + str(game_mode) +")")
    print(("  "*(int(PLAYER_STATS_LINES_FACTOR*map.global_columns)))+("PLAYER 1" if (game_mode == GAME_MODE_P_VS_P) or (game_mode == GAME_MODE_P_VS_AI) else "COM 1")+ (" "*((PLAYER_STATS_COLUMNS_FACTOR*map.global_columns)-4)) +("PLAYER 2" if (game_mode == GAME_MODE_P_VS_P)  else ("COM" if (game_mode == GAME_MODE_P_VS_AI) else "COM 2"))+"\n")
    p1_points, p1_ghosts = get_player_stats(PLAYER_1)
    p2_points, p2_ghosts = get_player_stats(PLAYER_2)
    print(("  "*(int(PLAYER_STATS_LINES_FACTOR*map.global_columns)-1))+ term.on_brown4("👻")+": " + ("%02d" % p1_ghosts) + " P: " + ("%02d" % p1_points) + (" "*((PLAYER_STATS_COLUMNS_FACTOR*map.global_columns)-10)) + term.on_darkolivegreen4("👻") + ": " + ("%02d" % p2_ghosts) + " P: " + ("%02d" % p2_points) + "\n")

if __name__ == '__main__':
    game_init(GAME_LINES, GAME_COLUMNS)