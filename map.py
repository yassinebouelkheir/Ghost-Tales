import os
import random
import blessed

term = blessed.Terminal()

ITEM_ADD = 0
ITEM_DELETE = 1
ITEM_CHANGE_ICON = 2

ITEM_TYPE_GHOST = 0
ITEM_TYPE_MAGIC = 1

ICON_GHOST = 0
ICON_MAGIC_1 = 1
ICON_MAGIC_2 = 2
ICON_MAGIC_3 = 3

MAP_STEP_CONST = 9
MAX_POSITIONS = 100

POSITION_ERROR_MARGE = 20
PLAYER_STATS_COLUMNS_FACTOR = 8
PLAYER_STATS_LINES_FACTOR = 0.2

global_border_horizontal = ''
global_border_vertical = ''
global_lines = 0
global_columns = 0

game_icons = ['👻', '🍄', '🌟', '👾']
positions = [[0 for x in range(MAX_POSITIONS)] for x in range(MAX_POSITIONS)]
position_state = [[0 for x in range(MAX_POSITIONS)] for x in range(MAX_POSITIONS)]

def generate_positions_list(lines, columns):
    if (lines < 2 or columns < 2) or (lines > 100 or columns > 100):
        raise TypeError("[map.py:generate_positions_list] Error 01: number of lines or columns is invalid (lines: " + str(lines) +" columns: " + str(columns) +")")
    
    global global_border_horizontal, global_border_vertical, positions
    if global_border_horizontal == '' or global_border_vertical == '':
        raise TypeError("[map.py:generate_positions_list] Error 06: vertical or horizontal borders are not defined, invalid map string")

    positions[0][0] = len(global_border_horizontal) + MAP_STEP_CONST
    for y in range(1, columns):
        positions[0][y] = positions[0][y-1] + MAP_STEP_CONST
    
    for x in range(1,lines):
        positions[x][0] = positions[x-1][0] + (len(global_border_horizontal)*2)
        for y in range(1, columns):
            positions[x][y] = positions[x][y-1] + MAP_STEP_CONST

def positions_update(x, y, fnc):
    for i in range(0, MAX_POSITIONS):
        for j in range(0, MAX_POSITIONS):
            if positions[i][j] != 0:
                if i == x:
                    if j > y:
                        positions[i][j] += fnc
                elif i > x:
                    positions[i][j] += fnc

def build_empty_map(lines, columns):
    if (lines < 2 or columns < 2) or (lines > 100 or columns > 100):
        raise TypeError("[map.py:build_empty_map] Error 01: number of lines or columns is invalid (lines: " + str(lines) +" columns: " + str(columns) +")")
    global global_border_horizontal, global_border_vertical, global_lines, global_columns
    border_horizontal, border_vertical, temp_separator = '', '', ''
    border_horizontal += '*********'
    for i in range(0, columns): 
        border_horizontal += '*********'
        if i == 0:
            border_vertical += '****' + '|        |'
            temp_separator += '****' + ' -------- '
        elif i == (columns-1):
            border_vertical += '        |' + '****' + '\n'
            temp_separator += '-------- ' + '****' + '\n'
        else:
            border_vertical += '        |' 
            temp_separator += '-------- '
        
    border_horizontal += '\n' + border_horizontal + '\n'
    temp_border_vertical = border_vertical
    for i in range(0, lines): 
        if i == 0:
            border_vertical = temp_separator + border_vertical + temp_border_vertical +  temp_border_vertical + temp_separator
        else:
            border_vertical += temp_border_vertical + temp_border_vertical + temp_border_vertical + temp_separator

    global_border_vertical = border_vertical
    global_border_horizontal = border_horizontal
    global_lines = lines
    global_columns = columns
    map_string = border_horizontal + border_vertical + border_horizontal
    print(map_string)

def map_update(new_border_vertical):
    global global_border_horizontal, global_border_vertical
    os.system('clear')
    global_border_vertical = new_border_vertical
    map_string = global_border_horizontal + global_border_vertical + global_border_horizontal
    print(map_string)

def item_update(x, y, update_type, item_type=-1, itemid=-1, playerid=-1, icon=-1):
    global global_border_horizontal, global_border_vertical, position_state
    position_error_correction = 0
    if x < 0 or y < 0:
        raise TypeError("[map.py:item_update] Error 02: line or column index is invalid (line: " + str(x) +" column: " + str(y) +")")
    if (icon != -1) and (icon > 3 or icon < 0):
        raise TypeError("[map.py:item_update] Error 03: invalid icon index (index: " + str(icon) +")")
    if update_type == ITEM_ADD:
        if item_type == ITEM_TYPE_GHOST:
            if playerid == 0:
                global_border_vertical = global_border_vertical[:positions[x][y]-4] + term.white_on_brown4(" " + (game_icons[icon] if icon != -1 else game_icons[ICON_GHOST]) + ("  %02d" % itemid) + " ") + global_border_vertical[positions[x][y]+4:]
            elif playerid == 1:
                global_border_vertical = global_border_vertical[:positions[x][y]-4] + term.white_on_darkolivegreen4(" " + (game_icons[icon] if icon != -1 else game_icons[ICON_GHOST]) + ("  %02d" % itemid) +" ") + global_border_vertical[positions[x][y]+4:]
            else: 
                raise TypeError("[map.py:item_update] Error 10: invalid playerid (playerid: " + str(playerid) +")")
        elif item_type == ITEM_TYPE_MAGIC:
            global_border_vertical = global_border_vertical[:positions[x][y]-4] + term.white_on_deepskyblue3(" " + (game_icons[icon] if icon != -1 else game_icons[random.randint(ICON_MAGIC_1, ICON_MAGIC_3)]) + ("  %02d" % itemid) +" ") + global_border_vertical[positions[x][y]+4:]
        else:
            raise TypeError("[map.py:item_update] Error 04: indefined item type (item_type: " + str(item_type) +")")
        position_state[x][y] = 1
        position_error_correction = POSITION_ERROR_MARGE
    elif update_type == ITEM_DELETE:
        global_border_vertical = global_border_vertical[:positions[x][y]-1] + ' ' + global_border_vertical[positions[x][y]+1:]
        position_state[x][y] = 0
        position_error_correction = -POSITION_ERROR_MARGE
    elif update_type == ITEM_CHANGE_ICON:
        if icon < 0 or icon > 3:
            raise TypeError("[map.py:item_update] Error 03: invalid icon index (index: " + str(icon) +")")
        else:
            raise TypeError("[map.py:item_update] Error 07: indefined item type (item_type: " + str(item_type) +")")
    else:
        raise TypeError("[map.py:item_update] Error 05: indefined update type (update_type: " + str(update_type) +")")
    map_update(global_border_vertical)
    positions_update(x, y, position_error_correction)