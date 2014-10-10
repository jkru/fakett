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

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Placed(GameElement):
    SOLID = True
    value = 0
#    def __init__(self):
#        horizontalcol = []
#        for i in range(3):
#            horizontalcol.append(GAME_BOARD.placed_pieces[self.y][i])
#        is_trip  = find_triples(horizontalcol,self.value,0)
#        if is_trip[1] and is_trip[2]:
#            if is_trip[0]==is_trip[1] and is_trip[2]==is_trip[0]:
#                set_triples_horiz()
#                GAME_BOARD.placed_pieces[self.y][self.x] = self.value+1



class PlacedRock(Placed):
    IMAGE = "Rock"
    value = 1

class PlacedGreenGem(Placed):
    IMAGE = "GreenGem"
    value = 2

class PlacedStar(Placed):
    IMAGE = "Star"
    value = 3


class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Piece(GameElement):
    is_placed = False
    def __init__(self, piece_type):
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
            #turn on flag
            self.is_placed = True

            #determine how to update matrix
            if self.piece_type == "Rock":
                the_type = 1
            elif self.piece_type == "GreenGem":
                the_type = 2
            elif self.piece_type == "Star":
                the_type = 3
            else:
                the_type = 0

            #update matrix
            self.board.placed_pieces[self.y][self.x] = the_type

            #check our matrix horizontally
            hc = []
            for j in range(1,6):
                hc.append(self.board.placed_pieces[self.y][j])

            hc_str = ''.join(str(e) for e in hc)
            if str(the_type)*3 in hc_str:
                print "*******************"
                print self.board.placed_pieces
                #create initial indices for where the 3 like-pieces are being placed
                for i in range(3):
                    three_like_types = find_triples(hc,the_type, i)
                    print "***three like types***"
                    print three_like_types
                    raw_input()
                    if three_like_types[1] and three_like_types[2]:
                        if three_like_types[0] == three_like_types[1] and three_like_types[0] == three_like_types[2]:  
                            set_triples_horiz(three_like_types)
                            GAME_BOARD.del_el(3,3)
                            GAME_BOARD.del_el(2,3)
                            GAME_BOARD.del_el(1,3)
                            break

                self.board.placed_pieces[self.y][self.x] = the_type+1

                print(self.board.placed_pieces[self.y][self.x],self.y,self.x,"hooray!")
                

            else:
                print("stuff")
            print("Horizontal Check")
            print self.board.placed_pieces

            putdownx = self.x
            putdowny = self.y

            if self.x + 2 <= GAME_WIDTH:
                GAME_BOARD.set_el(putdownx+1,putdowny, self)
            elif self.y + 2 <= GAME_HEIGHT:
                GAME_BOARD.set_el(putdownx,putdowny+1, self)

            if self.piece_type == "Rock":
                placed_piece = PlacedRock()
            elif self.piece_type == "GreenGem":
                placed_piece = PlacedGreenGem()
            elif self.piece_type == "Star":
                placed_piece = PlacedStar()
            GAME_BOARD.register(placed_piece)
            GAME_BOARD.set_el(putdownx, putdowny, placed_piece)

            
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
def find_triples(board_col, the_type, start):
    try:
        first_oc = board_col.index(the_type, start)
        second_oc = board_col.index(the_type, first_oc+1)
        third_oc =  board_col.index(the_type, second_oc+1)
        return [first_oc, second_oc, third_oc]
    except:
        pass
    return([0,1,2])

def set_triples_horiz(trips):
    first_oc, second_oc, third_oc = trips 
    GAME_BOARD.placed_pieces[self.y][first_oc] = 0
    GAME_BOARD.placed_pieces[self.y][second_oc] = 0
    GAME_BOARD.placed_pieces[self.y][third_oc] = 0

    GAME_BOARD.del_el(first_oc ,self.y)
    GAME_BOARD.del_el(second_oc,self.y)
    GAME_BOARD.del_el(third_oc ,self.y)
    raw_input("In the triples")

def make_random_piece():
    random_piece_class = random.choice(["Star","GreenGem","Rock"])
    raw_input(random_piece_class)

    if random_piece_class == "Rock":
        random_piece = Rock()
    elif random_piece_class == "GreenGem":
        random_piece = GreenGem()
    else:
        random_piece = Star()
    return(random_piece)



def initialize():
    """Put game initialization code here"""

    tree_positions = []

    for i in range(7):
        tree_positions.append([0,i])
    for i in range(1,7):
        tree_positions.append([i,0])
    for i in range(1,7):
        tree_positions.append([6,i])
    for i in range(1,6):
        tree_positions.append([i,6])

    new_piece = make_random_piece()
    GAME_BOARD.register(new_piece)
    GAME_BOARD.set_el(4,4, new_piece)


    trees = []
    for pos in tree_positions:
        tree = ShortTree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)

    # a_piece = make_random_piece()
    # GAME_BOARD.register(a_piece)
    # first_x = random.randint(1,5)
    # first_y = random.randint(1,5)
    # GAME_BOARD.set_el(first_x,first_y,a_piece)

    GAME_BOARD.placed_pieces = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]


    print ("this is the game board init")
    print GAME_BOARD.placed_pieces

         #   GAME_BOARD.placed_pieces[i].append([0,0,0,0])


    #get some sort of method from the piece class
    #to then modify board matrix

    


