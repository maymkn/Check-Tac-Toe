from utils import load_image
class Pieces:
    def __init__(self, sprite):
        self.sprite = sprite

    #def place_piece(surface, self.sprite, position):
        

class Blue(Pieces):
    def __init__(self):

        super().__init__(load_image("blue-circle", False))
                         
class Red(Pieces):
    def __init__(self):
        super().__init__(load_image("red-circle", False))


#this is unncessary. but i just wanted to play around with inheritance
#or maybe for scalability if there's ever a need

#coud have used pygame.draw.circle(...color...) instead of sprites.
#begets better results but i stuck with my mistake.