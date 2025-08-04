import pygame
from utils import load_image, clickable_positions
from models import Blue, Red
from pygame.math import Vector2 
from random import randint

INF = float('inf') #to be used instead of none. for filling up empty board
class Check_Tac_Toe:
    """A game like tic-tac-toe but not quite. A game like checkers but not quite. The winning configurations are exactly like TTT's and moves
    almost like checkers. The difference with tic-tac-toe is that each player is limited to 3 pieces. Once all the pieces are played on the board
    in turns, the next motions are by sliding, just like checkers, except no jumping over or capturing pieces. A piece can move to an adjacent
    empty horizontal, vertical or diagonal position. Slide along the lines indicated on the board. (The board is ugly. My first attempt at using
    blender, which I swear to never touch again).  Slide as long as possible until one player wins. There's only a limited number of configur-
    ations possible on the board so the game definitely has a magic sequence of steps to follow to always win. Homework!
    
    Mayen Magot"""

    def __init__(self):

        self.__init__pygame()
        self.screen = pygame.display.set_mode((600,600))
        self.clock = pygame.time.Clock()
        self.background = load_image("grid", False)


        #the game board. pieces to be placed in it. 
        #the two players are 1 and 0 for ease of everything. inf because i'll use row/col/diag summation to figure out the winner later
        self.board = [[INF, INF, INF], 
             [INF, INF, INF],
             [INF, INF, INF]]
        self.positions = [[(0,0), (290,0), (580,0)], 
                          [(0,290), (290,290), (580,290)], 
                          [(0,580),(290,580),(580,580)]]
        #the game board is 3 by 3. indices in self.positions are where the pieces on the board are to be drawn

        self.piece_corners = [(0,0), (290,0), (580,0), (0,290), (290,290), (580,290), (0,580),(290,580),(580,580)]
        self.active_positions = clickable_positions()
        #seems unnecessary but the way pygame detects collisions mandates this mess. i'll use the piece_corners to get the rects of length 20
        #which will then be stored in active positions. a direct match in indexing. the index of a clicked position in active_positions
        #is the same as that in piece corners. and then a//b,a%b gets me indices in positions and board. there might be a better way to do it.
        #it will not be figured out by me.
        

        #all the winning positions for 3 by 3. direct comparison is quicker but scalability issues. might try a 4 * 4 grid. saving this for later
        self.win_indices_array = [[(0,0),(1,1),(2,2)], 
                                [(0,2),(1,1),(2,0)],
                                [(0,0),(1,0),(2,0)],
                                [(0,1),(1,1),(2,1)],
                                [(0,2),(1,2),(2,2)],
                                [(0,0),(0,1),(0,2)],
                                [(1,0),(1,1),(1,2)],
                                [(2,0),(2,1),(2,2)]]


        self.blue = Blue() #the blue circle (which is somehow a rectangle because pygame!)
        self.red = Red() #red

        self.current_player = randint(0,1) #current player
        self.winner = None 
        #tracks the moves. each player needs 3 pieces each. a better way to limit that with just if else than messing with pygame Groups(). 
        # i don't want to know about them

        self.moves = 0
        self.selected_piece = None #yes, the selectec piece
        message = ''

    def draw_objects(self):
        #draws objects in their corresponding positions
        for i, row in enumerate(self.board):
            for j, obj in enumerate(row):
                if obj != INF:
                    position = Vector2(self.positions[i][j])
                    #apparently, self.red is an instance. so i have to access it's sprite manually by .sprite
                    piece = self.red.sprite if obj==1 else self.blue.sprite # 1 red, 0 blue
                    self.screen.blit(piece, position) #draw it on the screen

    def animate_piece_movement(self):
        pass
    #show piece movement from one position to another. will do it another day. 

    def check_winner(self):

        for line in self.win_indices_array:
            sum_line = sum(self.board[i][j] for i,j in line)

            if sum_line in {0,3}:
                self.winner = 'RB'[sum_line == 0] #R for red, B for Blue
                #works because  sum_line==0 true or false. true = 1 thus B, false = 0 thus R. 

                #unpacking to avoid type-error: indices can't be tuples
                # + (10,10) offsets the line position to the center of the clickable position since length = 20
                i0,j0 = line[0] #the start of the line
                i2,j2 = line[2] #the end of the line.
                self.winner_line = [Vector2(self.positions[i0][j0]) + Vector2(10,10), Vector2(self.positions[i2][j2]) + Vector2(10,10)]
                #start and end

    def draw_winner(self):

        if self.winner:
            line_color = 'red' if self.winner == 'R' else 'blue'
            pygame.draw.line(self.screen, line_color, *self.winner_line, 5) #on the screen, color, the start, the stop, the width
            #draws a line through a winning configuration. tomato is a weird color to like, i know. please don't judge me.

    def neighbours(self, i, j): #neighbours of a current position i,j on board

        _array = [(i,j-1),(i,j+1),(i-1,j), (i-1,j+1),(i+1,j-1),(i+1,j)]
        if +(i-j) != 1:
            _array. append((i+1,j+1))
            _array.append((i-1, j-1))
        return [self.positions[x][y] for x,y in _array if 0<=x<3 and 0<=y<3 and self.board[x][y] == INF]
    
    #+(x-y) is for handling the mid positions, top bottom left right.  somehow, the abs of diff in their i-j is 1. have to exploit that
    #there's no more elegant way than this!
    #and just realized that piece_corners is unnecessary. redifine active_positions with self.positions instead. would work with a 
    #few tweaks
         
    def move_piece(self,i,j,k,l): 
        #i,j => indices of current position, k,l => indices of position to move pieces to. 
        # #will redefine them into a class variables current_position and next_position should there arise a need.
        self.board[k][l] = self.board[i][j] #new position = current
        self.board[i][j] = INF #reset it
        
    def draw_text(self, message):

        pygame.font.init()
        font = pygame.font.Font(None, 50)
        text_surface = font.render(message, True, (0,0,0), None)
        rect_text = text_surface.get_rect()
        x, y = rect_text.width//2, rect_text.height//2
        self.screen.blit(text_surface, Vector2(self.screen.get_rect().center) - Vector2(x,y))



    def update_game_status(self):
        #calls the major game events; move, check
        self.moves += 1
        self.check_winner() #anyone won?
        self.current_player ^= 1 #switches players after a move
        pygame.display.set_caption(f"Grid Game              Player {'BR'[self.current_player]}'s turn!") 



    #runs the game. the major funtions
    def main_loop(self):
        while True:
            self._process_game_logic()
            self._handle_input()
            self._draw()



    #the key game functions
    def _process_game_logic(self):
    
        #clicked = Vector2(pygame.mouse.get_pos()) #a variable i commented out. might mess things up
        left_click = pygame.mouse.get_pressed()[0] #is mouse clicked? t,f
        corner = None #the corner of the current clicked position.
        for position in self.active_positions:
            if (position.collidepoint(Vector2(pygame.mouse.get_pos()))): #if a position clicked, find its corner 
                corner = position.topleft #yes, the topleft
                break
        
        if corner and left_click and not self.winner: #as it says
            i,j = divmod(self.piece_corners.index(corner), 3) #converts the index in piece_corners into board index
            k,l = None, None #indices for position to move the piece to. yet to be figured out

            if  self.moves <=5:
                #each player has 3 pieces. so stopping at 6 will give each player 3. the rest to be handled by else
                if self.board[i][j] == INF:
                    self.board[i][j] = self.current_player  

                    self.update_game_status()
    

            #the main game. past 6 moves
            elif self.moves > 5:
                #is there a selected piece? nope? then the current player selects it from his positions
                if self.selected_piece is None:
                    if self.board[i][j] == self.current_player:
                        self.selected_piece = (i,j) #yes, selected
                else:
                    si, sj = self.selected_piece #if a piece selected, indices of the selected piece
                    _valid_neighbours = self.neighbours(si, sj) #the neighbours of the selected position
                    for position in _valid_neighbours:
                        p = self.piece_corners.index(position)
                        #could have filled valid neighbours with tuples and then 3i + j to find p. realized a little too late. 

                        #detects point click on left click
                        if ((self.active_positions[p]).collidepoint(Vector2(pygame.mouse.get_pos()))) and left_click:
                            k,l = divmod(self.piece_corners.index(position), 3) 
                            self.move_piece(si,sj,k,l)    

                            #this needs to be a single function
                            self.update_game_status()

                            self.selected_piece = None #reset selected piece
                            break #yes
                    

    def _handle_input(self):

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                quit()
            
        #handles quit only now. wanna make the pieces movable by button clicks. a job for another day. 1,3,7,9 diag  2 4 6 8 horz,vert
        #key.get_pressed() or event.get
        
        

    def __init__pygame(self):
        pygame.init() #i have no choice
        pygame.display.set_caption('Welcome!')
        

    def _draw(self):
        self.screen.blit(self.background, (0,0)) #draws the background
        self.draw_objects() #draws the objects
        self.draw_winner() #draws the winner
        if self.winner:
            if self.winner == 'R':
                message= 'Osim won!'
            elif self.winner == 'B':
                message = 'Mayen won!'
                #message = f"Player {self.winner} won"
            self.draw_text(message)
            pygame.display.set_caption(f"Grid Game              Game Over!")
        pygame.display.flip() #refreshes the drawings
        self.clock.tick(60)

#merci beacoup for reading to the end! comments?
