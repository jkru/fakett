import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################


##set the size of the game board

GAME_WIDTH = 4
GAME_HEIGHT = 4

#### Put class definitions here ####

class Piece(GameElement):
    def __init__(self, piece_type):
        #pick which piece type
        # self.piece_type = random.choice(["Rock","GreenGem","Star"])
        # IMAGE = self.piece_type
        self.piece_type = piece_type
        GAME_BOARD.draw_msg("You just acquired a %s! Move your piece with the arrow keys and place with spacebar" % self.piece_type)
        print(self.piece_type)

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        elif direction == "putdown":
            return (self.x, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):

        direction = None

        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"
        elif symbol == key.SPACE:
            direction = "putdown"

        
        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                existing_el = self.board.get_el(next_x, next_y)

                if existing_el:
                    existing_el.interact(self)

                if existing_el and existing_el.SOLID:
                    self.board.draw_msg("There is something in my way!")

                elif existing_el is None or not existing_el.SOLID:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)

        if direction == "putdown":
            GAME_BOARD.register(self)
#            make_random_piece()
            

            # new_piece = [next_x, next_y, self.piece_type]
            # x,y, piece_type = new_piece



class Rock(Piece):
    IMAGE = "Rock"
    def __init__(self):
        self.piece_type = "Rock"
        return super(Rock, self).__init__("Rock")

class GreenGem(Piece):
    IMAGE = "GreenGem"
    def __init__(self):
        self.piece_type = "GreenGem"
        return super(GreenGem, self).__init__("GreenGem")

class Star(Piece):
    IMAGE = "Star"
    def __init__(self):
        self.piece_type = "Star"
        return super(Star, self).__init__("Star")


####   End class definitions    ####
# def make_random_piece():
#     first_piece_class = random.choice(["Rock","Star","GreenGem"])
#     if first_piece_class == "Rock":
#         first_piece = Rock()
#     elif first_piece_class == "GreenGem":
#         first_piece = GreenGem()
#     else:
#         first_piece = Star()
#     return(first_piece)



def initialize():
    """Put game initialization code here"""

    a_piece_class = random.choice(["Rock","Star","GreenGem"])
    if a_piece_class == "Rock":
         a_piece = Rock()
    elif a_piece_class == "GreenGem":
         a_piece = GreenGem()
    else:
         a_piece = Star()

#    a_piece = make_random_piece()
    GAME_BOARD.register(a_piece)
    first_x = random.randint(0,3)
    first_y = random.randint(0,3)
    GAME_BOARD.set_el(first_x,first_y,a_piece)



def tripletown():
        #initialize matrix to 0, for nothing in it
    board_matrix = []
    for i in range(GAME_WIDTH):
        board_matrix.append([])
        for j in range(GAME_HEIGHT):
            board_matrix[i].append([0,0,0,0])

    print(board_matrix)




    #get some sort of method from the piece class
    #to then modify board matrix

    


