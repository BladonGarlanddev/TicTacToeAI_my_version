import pygame as game
import sys
import time
import copy
from IPython import embed
import pdb

running = True
XO = "x"

width = 400

height = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

line_color = (0, 0, 0)

board = [[None] * 3, [None] * 3, [None] * 3]

game.init()

screen = game.display.set_mode((width, height + 100), 0, 32)

score = 0

game_over = False

winning_spaces = []

moves = 0

def draw_status(winner):

    # getting the global variable draw
    # into action

    message = None

    if game_over is False:
        message = XO.upper() + "'s Turn"
    elif not winner:
        message = "Game Draw !"
    else:
        message = winner.upper() + " won !"
    

    print(f"MESSAGE: {message}")

    # setting a font object
    font = game.font.Font(None, 30)

    # setting the font properties like
    # color and width of the text
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    game.display.update()


def draw_board():
    screen.fill(WHITE)
    # Draw grid lines
    game.draw.line(screen, BLACK, (width / 3, 0), (width / 3, height), 7)
    game.draw.line(screen, BLACK, (2 * width / 3, 0), (2 * width / 3, height), 7)
    game.draw.line(screen, BLACK, (0, height / 3), (width, height / 3), 7)
    game.draw.line(screen, BLACK, (0, 2 * height / 3), (width, 2 * height / 3), 7)

    # Draw the Xs and Os
    for row in range(3):
        for col in range(3):
            if board[col][row] == "x":
                game.draw.line(
                    screen,
                    BLACK,
                    (col * width / 3 + 50, row * height / 3 + 50),
                    ((col + 1) * width / 3 - 50, (row + 1) * height / 3 - 50),
                    7,
                )
                game.draw.line(
                    screen,
                    BLACK,
                    ((col + 1) * width / 3 - 50, row * height / 3 + 50),
                    (col * width / 3 + 50, (row + 1) * height / 3 - 50),
                    7,
                )
            elif board[col][row] == "o":
                game.draw.circle(
                    screen,
                    BLACK,
                    (
                        int(col * width / 3 + width / 6),
                        int(row * height / 3 + height / 6),
                    ),
                    width // 6 - 50,
                    7,
                )
    game.display.update()


def check_game_status(BOARD):
    global game_over, winning_spaces, XO

    # An array of arrays where each sub array consists of coordinates. Each sub array creates a scorable pattern
    lines = [
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(2, 0), (1, 1), (0, 2)],
        # Columns
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Rows
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
    ]

    winning_space = None
    # Check each line for a win
    score_buffer = 0

    # idx is the index of the for loop. Line is the value of lines at idx and is an array of coordinates
    for idx, line in enumerate(lines):

        reference_value = None
        inline_spaces = 0

        for col, row in line:
            # checks the literal value of the psuedo board at the coordinates
            space_value = BOARD[col][row]

            # if the space we checked is none, it could potentially be the square that needs played to be a winner
            if space_value is None:
                winning_space = {"col": col, "row": row}
                print("1")

            # space_value was not none so we check to see if there was a reference value to compare it to. if reference value is equal to space_value, that means there was a space before it that was owned by the same character as the space we are checking now
            elif reference_value == space_value:
                inline_spaces += 1
                print("2")

            # space_value is not none but is also not equal to reference value. reference_value is either None or it is equal to the opposite player as space_value.
            elif reference_value:
                print("3")
                inline_spaces = 0
                continue
                # this means x and o existed in the same pattern which means the pattern is unwinnable. Exit the for loop to save compute time.

            # space_value was not None, space_value was not equal to reference value, reference value was empty
            else:
                reference_value = space_value
                inline_spaces = 1
                print("4")
                # this means space_value is the only owned space within the pattern so far. Make it the reference value

            print(
                f"index: {idx}, col: {col}, row: {row}, space_value: {space_value}, board_val: {BOARD[col][row]}, referenence_value: {reference_value}, inline_spaces: {inline_spaces}\n"
            )

        # provide a score for the pattern we just evaluated
        if reference_value == 'x':
            # this board has been won by x
            if inline_spaces == 3:
                score_buffer = 1
                break
            elif inline_spaces == 2:
                score_buffer += .5
                winning_spaces.append(
                    {
                        "col": winning_space["col"],
                        "row": winning_space["row"],
                        "player": "x",
                    }   
                )
                print(f"\nwinning space found: [{col}, {row}], player: x")

        else:
            # this board has been won by o
            if inline_spaces == 3:
                score_buffer = -1
                break
            elif inline_spaces == 2:
                score_buffer += -.5
                winning_spaces.append(
                    {
                        "col": winning_space["col"],
                        "row": winning_space["row"],
                        "player": "o",
                    }
                )
                print(f"\nwinning space found: [{col}, {row}], player: o")

    print(f"Score_buffer: {score_buffer}\n")

    # winning_space could only be [] if there were no empty spaces in any of the patterns
    if winning_space == None:

        # if there were no empty spaces and the score was not 1 or -1
        if abs(score_buffer) != 1:
            return "draw", None, score_buffer
    else:
        print(f"winning_space: {winning_space}")


    if score_buffer == 1:
        return "win", 'x', score_buffer
    elif score_buffer == -1:
        return "win", 'o', score_buffer

    # there were more empty spaces and the score was not 1 or -1
    else:
        return None, None, score_buffer


def make_move(col, row):
    global moves, XO, winning_spaces
    
    #if the current player is 'x
    if XO == "x":
        #if the position being played is empty
        if board[col][row] is None:
            board[col][row] = "x"
            moves += 1
            #make it player 'o's turn
            XO = "o"
            print(f"Move made at [{col}, {row}]")
        else:
            from IPython.core.debugger import Pdb

            Pdb().set_trace()
            raise Exception(
                "You tried to play a square that was already taken at position [{}, {}] Position already claimed by {}".format(
                    col, row, board[col][row]
                )
            )
    else:
        if board[col][row] is None:
            board[col][row] = "o"
            moves += 1
            XO = "x"
            print(f"Move made at [{col}, {row}]")
        else:
            from IPython.core.debugger import Pdb
            Pdb().set_trace()
            raise Exception(
                "AI tried to play a square that was already taken at position [{}, {}]. Position already claimed by {}".format(
                    col, row, board[col][row]
                )
            )
    winning_spaces = []

def ai_move():
    global moves, XO, winning_spaces
    if moves == 1:
        if board[1][1] == None:
            make_move(1, 1)
            return True

    best_move = None
    best_score = score

    #checks to see if there are winning spaces
    if winning_spaces:
        #pdb.set_trace()
        #iterates through winning spaces
        for item in winning_spaces:
            #executes if the winning space is winning for player o
            if item["player"] == "o":
                print(
                    f"winning space: [{item['col']}, {item['row']}], player: {item['player']}"
                )
                make_move(item["col"], item["row"])
                return None
            else:
                #otherwise, save the coordinates of a winning space for player x
                best_move = [item["col"], item["row"]]

        #None of the winning moves were for player o, play a preventitive move against x
        print(
            f"winning space: [{item['col']}, {item['row']}], player: {item['player']}"
        )
        make_move(best_move[0], best_move[1])
        return None
    else:
        #no winning spaces exist. Check all possible board states at the current depth
        for col in range(3):
            for row in range(3):
                #if board[col][row] is an empty space
                if board[col][row] is None:
                    #create a copy of the board
                    new_board_state = copy.deepcopy(board)
                    #set an empty space to 'o'
                    new_board_state[col][row] = "o"
                    #evaluate the score of the theorhetical board
                    board_score = check_game_status(new_board_state)[2]
                    print(f"Col: {col}, Row: {row}, board_score: {board_score}")
                    #because 'o' is the minimizing player, you should check and see if the score of the theorhetical board is lower than best score where best score starts as the actual score 
                    if board_score < best_score:
                        best_score = board_score
                        best_move = [col, row]

        #if a move that would improve the score was found:
        if best_move is not None:
            make_move(best_move[0], best_move[1])
            return None
        else:
            #check all squares on the board until an empty square is found, then play it
            for col in range(3):
                for row in range(3):
                    if board[col][row] is None:
                        make_move(col, row)
                        return None
    return False


def play():
    global XO, game_over
    status_changed = False
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                sys.exit()
            elif game_over is False:
                if XO == "o":
                    ai_move()
                    status_changed = True
                elif event.type == game.MOUSEBUTTONDOWN:
                    status_changed = True
                    mouseX, mouseY = event.pos
                    col = mouseX // (width // 3)
                    row = mouseY // (height // 3)

                    if board[col][row] is None:
                        make_move(col, row)

                if status_changed:
                    winner = None
                    status, player, score = check_game_status(board)

                    if status is not None:
                        game_over = True
                        winner = player
                        print(f"SOMEONE WON AND IT WAS PLAYER: {player}")
                    status_changed = False
                    draw_board()
                    draw_status(winner)
                    print("NEW ITERATION \n")


# Initial drawing of the board
# Main game loop
play()

game.quit()
