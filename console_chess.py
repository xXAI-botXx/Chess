import sys

import Engine.chess_engine as engine
import Engine.chess_men as pieces
import io_helper as io

commands = {'exit':lambda x:exit(x), 'start':lambda x:start(x), 'turn':lambda x:turn(x), 'move':lambda x:turn(x),
            'save':lambda x:save(x), 'load':lambda x:load(x), 'help':lambda x:help(x)}
cur_engine = None

def turn(user_input:str):
    global cur_engine
    if len(user_input.split(" ")) == 3:
        if cur_engine != None:
            from_pos, to_pos = user_input.split(" ")[1], user_input.split(" ")[2]
            cur_engine.run_move(from_pos, to_pos)
        else:
            io.print_with_only_delay("You have to start a new Game!", 0, 0)
    else:
        io.print_with_only_delay("Not a valid turn", 0, 0)

def show():
    field = cur_engine.get_field()
    show_field = ""
    for row in range(8, 0, -1):
        for line in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            pos = f"{line}{row}"

            if pos[0] == "a":
                show_field += f"{pos[1]} |"

            if field[pos] == None:
                show_field += " + "
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
        cur_engine = engine.Engine(new_game=True, mode=engine.modes.CLASSIC)
        #show()

def save(user_input:str):
    pass

def load(user_input:str):
    pass

def help(user_input:str):
    txt = "Welcome to the help section."
    txt += "\n\nThere are following Commands:"
    txt += "\n    - start"
    txt += "\n    - move {from pos} {to pos}"
    txt += "\n    - save"
    txt += "\n    - load"
    txt += "\n    - help"
    txt += "\n    - exit"
    io.print_with_only_delay(txt)
    io.confirm(f"(Press {io.RED}Enter{io.END} to confirm)", cleanup=True, fast=True)

def exit(user_input:str):
    sys.exit(0)

def run():
    global cur_engine
    #print(f"{io.CLEAR_SCREEN(2)}{io.SET_POSITION(0, 0)}")
    #io.print_char_with_only_delay("Start Console Chess...")

    while True:
        print(f"{io.CLEAR_SCREEN(2)}{io.SET_POSITION(0, 0)}")
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
        except KeyError:
            user_input = io.print_with_only_delay("Input not found! Try again.", 0, 0)
            io.confirm(f"Press {io.BACKGROUND_RED}Enter{io.END} to confirm", fast=True)


if __name__ == '__main__':
    run()