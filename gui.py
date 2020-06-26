import pygame

clock = pygame.time.Clock()
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((512,512))



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class displaytextbox:
    def __init__(self):
        self.posx=0
        self.posy=0
        self.color=white
        self.txtcolor=black
        self.height=30
        self.width=200
        self.text=""
        self.rct=pygame.Rect(self.posx,self.posy,self.width,self.height)
        self.active=False
        self.done = False
        self.edit=True
        self.controltext=""

class clickbox(displaytextbox):
    pass
    def main(self):

        self.rct = pygame.Rect(self.posx, self.posy, self.width, self.height)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.rct.collidepoint(event.pos):

                        self.active = not self.active
                    else:
                        self.active = False

                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            self.done = True
                        elif event.key == pygame.K_BACKSPACE and self.edit==True:
                            self.text = self.text[:-1]
                        elif self.edit==True:
                            self.text += event.unicode

            screen.fill((30, 30, 30))
            txt_surface = font.render(self.text, True, self.color)
            width = max(200, txt_surface.get_width() + 10)
            clickbox.w = width
            screen.blit(txt_surface, (self.posx + 5, self.posy + 5))
            pygame.draw.rect(screen, self.color, self.rct, 2)
            draw_text(self.controltext, font, (255, 255, 255), screen, 100, 20)
            pygame.display.flip()
            clock.tick(30)
        return self.text