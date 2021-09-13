import sys
import os

import Engine.chess_engine as engine
import Engine.chess_men as pieces
import io_helper as io

commands = {'exit':lambda x:exit(x), 'start':lambda x:start(x), 'turn':lambda x:turn(x), 'move':lambda x:turn(x),
            'save':lambda x:save(x), 'load':lambda x:load(x), 'help':lambda x:help(x), 'show':lambda x:show_saves(x),
            'new':lambda x:new_game(x), 'break':lambda x:break_game(x), 'saves':lambda x:show_saves('show saves')}
cur_engine = None

def turn(user_input:str):
    global cur_engine
    if len(user_input.split(" ")) == 3:
        if cur_engine != None:
            from_pos, to_pos = user_input.split(" ")[1], user_input.split(" ")[2]
            result = cur_engine.run_move(from_pos, to_pos)
            if len(result[1]) > 0:
                show()
                io.print_with_only_delay(result[1], 0, 0)
                io.confirm(f"\n(Press {io.RED}Enter{io.END} to continue.)", True, True)
        else:
            io.print_with_only_delay("You have to start a Game!", 0, 0)
    elif len(user_input.split(" ")) == 2:
        if cur_engine != None:
            from_pos = user_input.split(" ")[1]
            result = cur_engine.get_moves(from_pos)
            if type(result) == str:
                io.print_with_only_delay("\n"+result, 0, 0)
                io.confirm(f"\n(Press {io.RED}Enter{io.END} to continue.)", True, True)
        else:
            io.print_with_only_delay("You have to start a Game!", 0, 0)
    else:
        io.print_with_only_delay("Not a valid turn", 0, 0)

# or the sites with color text showing
def show():
    io.print_with_only_delay(f"{io.CLEAR_SCREEN(2)}{io.SET_POSITION(0, 0)}", 0, 0)
    field = cur_engine.get_field()
    show_field = ""
    for row in range(8, 0, -1):
        for line in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            pos = f"{line}{row}"

            if pos[0] == "a":
                show_field += f"{pos[1]} |"

            if field[pos] == None:
                show_field += "   "
            elif type(field[pos]) == pieces.Pawn:
                if field[pos].site == engine.site.WHITE:
                    show_field += " P "
                else:
                    show_field += "_P_"
            elif type(field[pos]) == pieces.Rook:
                if field[pos].site == engine.site.WHITE:
                    show_field += " R "
                else:
                    show_field += "_R_"
            elif type(field[pos]) == pieces.Knight:
                if field[pos].site == engine.site.WHITE:
                    show_field += " N "
                else:
                    show_field += "_N_"
            elif type(field[pos]) == pieces.Bishop:
                if field[pos].site == engine.site.WHITE:
                    show_field += " B "
                else:
                    show_field += "_B_"
            elif type(field[pos]) == pieces.Queen:
                if field[pos].site == engine.site.WHITE:
                    show_field += " Q "
                else:
                    show_field += "_Q_"
            elif type(field[pos]) == pieces.King:
                if field[pos].site == engine.site.WHITE:
                    show_field += " K "
                else:
                    show_field += "_K_"
            
            if pos[0] == "h":
                show_field += "\n"

    show_field += "   ------------------------\n"
    show_field += "    a  b  c  d  e  f  g  h\n\n"

    io.print_with_only_delay(show_field, 0, 0)


def start(user_input:str):
    if len(user_input.split(" ")) == 1:
        global cur_engine
        if cur_engine == None:
            cur_engine = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)
        else:
            io.print_with_only_delay("\nYou are still playing a chess game!", 0, 0.5)

def new_game(user_input:str):
    if user_input.lower() == "new game":
        start("start")

def break_game(user_input:str):
    global cur_engine
    if cur_engine != None:
        cur_engine = None
        io.print_with_only_delay("the game has been quit. Now you are in the main menu.\n", 0, 0)
        io.press_enter_to_confirm()  

def save(user_input:str):
    if len(user_input.split(" ")) == 2:
        if cur_engine != None:
            if user_input.split(" ")[1].endswith(".txt"):
                filename = user_input.split(" ")[1]
            else:
                filename = user_input.split(" ")[1]+".txt"

            chess_game = cur_engine.get_game_log()

            with open("./SAVES/"+filename, mode="w") as f:
                f.write(chess_game)
                io.print_with_only_delay("This game is saved. Enjoy it in the future :D\n", 0, 0)
                io.press_enter_to_confirm()  
        else:
            io.print_with_only_delay("You have to be in a game, to can save the game...\n", 0, 0)
            io.press_enter_to_confirm()  
    else:
        io.print_with_only_delay("You have to write 'save *filename*' without the stars.\n", 0, 0)
        io.press_enter_to_confirm()  

def load(user_input:str):
    global cur_engine

    if len(user_input.split(" ")) == 2:
        if user_input.split(" ")[1].endswith(".txt"):
            filename = user_input.split(" ")[1]
        else:
            filename = user_input.split(" ")[1]+".txt"

        try:
            with open("./SAVES/"+filename, mode="r") as f:
                chess_game = f.read().split("\n")
                global cur_engine
                cur_engine = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)   
                result, messages = cur_engine.run_many_moves(chess_game)
                if result == False:
                    cur_engine = None
                io.print_with_only_delay(messages, 0, 0)
                io.press_enter_to_confirm()  
        except FileNotFoundError:
            io.print_with_only_delay("I can't found this Save.\n Try again.\n", 0, 0)
            io.press_enter_to_confirm()
    elif len(user_input.split(" ")) == 3 and (user_input.split(" ")[1].lower() == "nr" or user_input.split(" ")[1].lower() == "nr."):
        try:
            filename = os.listdir("./SAVES")[int(user_input.split(" ")[2])-1]
        except IndexError:
            return (False, "I don't found this Save! Please try again.")
        try:
            with open("./SAVES/"+filename, mode="r") as f:
                chess_game = f.read().split("\n")
                cur_engine = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)   
                result, messages = cur_engine.run_many_moves(chess_game)
                if result == False:
                    cur_engine = None
                io.print_with_only_delay(messages, 0, 0)
                io.press_enter_to_confirm()  
        except FileNotFoundError:
            io.print_with_only_delay("I can't found this Save.\n Try again.\n", 0, 0)
            io.press_enter_to_confirm()

def show_saves(user_input:str):
    if len(user_input.split(" ")) == 2 and user_input == "show saves":
        message = "\nChess Saves:"
        for i, file in enumerate(os.listdir("./SAVES")):
            if file.endswith(".txt"):
                message += f"\n    - {file} ({i+1})"
        message += "\n\n"
        message += "Hint: You can type 'load nr 1' to load the first Savegame (and with the others in the list so go on...)\n"
        io.print_with_only_delay(message, 0, 0)
        io.press_enter_to_confirm()

def help(user_input:str):
    txt = "Welcome to the help section."
    txt += "\n\nThere are following Commands:"
    txt += "\n    - start"
    txt += "\n    - move {from pos} {to pos}"
    txt += "\n        -> without the { }"
    txt += "\n        -> ingame available"
    txt += "\n    - save *filename*"
    txt += "\n        -> ingame available"
    txt += "\n    - load *filename*"
    txt += "\n        -> or use: load nr *filenr* -> see the nr in the () behind with the output of the 'show saves'"
    txt += "\n    - show saves"
    txt += "\n    - saves (as an shorter alternative)"
    txt += "\n    - help"
    txt += "\n    - exit"
    txt += "\n        -> ingame available, too"
    txt +=f"\n\nTip: type as example {io.PURPLE}move a3{io.END} to get the possible moves of this chess-piece"
    io.print_with_only_delay(txt, 0, 1)
    io.confirm(f"(Press {io.RED}Enter{io.END} to confirm)", cleanup=True, fast=True)

def exit(user_input:str):
    sys.exit(0)

def run():
    global cur_engine
    #print(f"{io.CLEAR_SCREEN(2)}{io.SET_POSITION(0, 0)}")
    #io.print_char_with_only_delay("Start Console Chess...")

    while True:
        print(f"{io.CLEAR_SCREEN(2)}{io.SET_POSITION(0, 0)}")
        if cur_engine != None and cur_engine.gameover == True:
            cur_engine = None

        if cur_engine != None:
            show()
            if cur_engine.get_active_player() == engine.site.WHITE:
                user_input = io.get_input("Player WHITE:")
            else:
                user_input = io.get_input("Player BLACK:")
        else:
            user_input = io.get_input("User input:")
        try:
            commands[user_input.split(" ")[0]](user_input)
        except KeyError as e:
            try:
                if engine.chessmen[user_input.upper()] in [engine.chessmen.KNIGHT, engine.chessmen.ROOK, engine.chessmen.BISHOP, engine.chessmen.QUEEN]:
                    if cur_engine != None:
                        result = cur_engine.pawn_promotion(user_input.upper())
                        if len(result[1]) > 0:
                            io.print_with_only_delay("\n"+result[1], 0, 0)
                            io.confirm(f"\n(Press {io.RED}Enter{io.END} to continue.)", True, True)
            except KeyError:
                #io.print_with_only_delay(e)
                io.print_with_only_delay(f"Input not found! Type {io.PURPLE}help{io.END} for all keywords.", 0, 0)
                io.confirm(f"(Press {io.RED}Enter{io.END} to continue)", fast=True)


if __name__ == '__main__':
    run()