from pygame.image import load
from pygame import Rect


def load_image(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_image = load(path)

    if with_alpha:
        return loaded_image.convert_alpha()
    else:
        return loaded_image.convert()
    
def clickable_positions():
    piece_corners = [(0,0), (290,0), (580,0), (0,290), (290,290), (580,290), (0,580),(290,580),(580,580)] 
    length = 20
    piece_rects = []

    for corner in piece_corners:
        x, y = corner
        rect = Rect(x, y, length , length)
        piece_rects.append(rect)
    return piece_rects



#nothing useful below this line. just a graveyard for my first attempts at indexing the board
#useless but sentimental information below this.





























def allowed_positions():

    tl, tm, tr = (0,0), (290,0), (580,0)
    ml, mm, mr = (0,290), (290,290), (580,290)
    bl, bm, br = (0,580),(290,580),(580,580)

    array = [[tl,tm,tr], [ml,mm,mr],[bl,bm,br]]

#the positions in record have to be linked to the positions on the surface
#clicking a position on board triggers appendage into the record board


    topleft, topmid, topright = (0,0), (290,0), (580,0)
    midleft, midmid, midright = (0,290), (290,290), (580,290)
    bottomleft, bottommid, bottomright = (0,580),(290,580),(580,580)

#adjacent_to:
#tl: tm, mm, ml tm: tl,tr,mm tr: tm,mm,mr
#ml: tl,mm,bl mm: all mr: tr,br,mm
#bl: ml,br,mm bm:bl,br,mm br:mr,bm,mm

#def is_occupied(): 

#let 1 = red, 0 = blue

board = [[None, None, None], 
             [None, None, None],
             [None, None, None]]




#checks if the mouse is over a clickable position

#if pygame.mouse.get_pressed():
           # clicked = pygame.mouse.get_pos()
            #for position in active_positions:
               # if position.collidepoint(clicked):
                 #   pygame.draw.rect(self.screen, (255,255,0), position)

#neighbours = [[(0,0),(0,1),(0,2)],
              #[(1,0),(1,1),(1,2)],
              #[(2,0),(2,1),(2,2)]]

#  for i,j neighbour = i+1,j  i,j+1  i+1, j+1   i-1,j  i,j-1, i-1,j-1

#def is_neighbour(other_which_is_now_board_ij):
   # array = [(i+1,j),(i,j+1),(i+1, j+1), (i-1,j),(i,j-1),(i-1,j-1)]
   #_valid_neighbours = [self.positions[x][y] for x,y in array if 0<=x<3 and 0<+y<3]
    #_neighbours = [self.positions[i] for i in array]
    #if clicked in neighbours
        #return True
   # return False

#not of any use. my first attempt at detecting winner
def winning_configurations():
                
    #diagonals
    [[(0,0),(1,1),(2,2)], 
     [(0,2),(1,1),(2,0)],
     [(0,0),(1,0),(2,0)],
     [(0,1),(1,1),(2,1)],
     [(0,2),(1,2),(2,2)],
     [(0,0),(0,1),(0,2)],
     [(1,0),(1,1),(1,2)],
     [(2,0),(2,1),(2,2)]]

     #efficient but unscalable
    if (board[0][0] == board[1][1] == board[2][2] or 
        board[0][2] == board[1][1] == board[2][0] or

        board[0][0] == board[1][0] == board[2][0] or 
        board[0][1] == board[1][1] == board[2][1] or
        board[0][2] == board[1][2] == board[2][2] or

        board[0][0] == board[0][1] == board[0][2] or
        board[1][0] == board[1][1] == board[1][2] or
        board[2][0] == board[2][1] == board[2][2]
        ):
        return #current_player
