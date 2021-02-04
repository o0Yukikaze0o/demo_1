import pygame
from pygame.locals import *
from components import Histogram, ProgressBar

RESOLUTION = (800,600)
CAPTION = 'Histogram Based Random Music Generator'
RED = (255,127,127)
GREEN = (127,255,127)
BLUE = (127,127,255)
GRAY = (127,127,127)
BLACK = (0,0,0)

pygame.init()
pygame.display.set_caption(CAPTION)
screen = pygame.display.set_mode(RESOLUTION)

defaultFont = pygame.font.SysFont('Arial',25)
TXT_PLAY = defaultFont.render(' || >',True,BLACK)
TXT_RANDOM = defaultFont.render('RAND',True,BLACK)
TXT_SAVE = defaultFont.render('SAVE',True,BLACK)

def print_button(screen,x,y,color,text):
    pygame.draw.rect(screen,color,[x,y,100,60])
    screen.blit(text,(x+5,y+10))

running = True
bg = BLUE
playing = False

screen.fill(bg)
print_button(screen,680,20,GRAY,TXT_PLAY)
print_button(screen,680,100,GRAY,TXT_RANDOM)
print_button(screen,680,180,GRAY,TXT_SAVE)
# y=260

while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == 27: # Esc
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 680 <= mouse[0] < 780 and 20 <= mouse[1] < 80:
                print_button(screen,680,20,GREEN,TXT_PLAY)
                playing = not playing
                print(playing)
            elif 680 <= mouse[0] < 780 and 100 <= mouse[1] < 160:
                print_button(screen,680,100,GREEN,TXT_RANDOM)
            elif 680 <= mouse[0] < 780 and 180 <= mouse[1] < 240:
                print_button(screen,680,180,GREEN,TXT_SAVE)
        elif event.type == pygame.MOUSEBUTTONUP:
            print_button(screen,680,20,GRAY,TXT_PLAY)
            print_button(screen,680,100,GRAY,TXT_RANDOM)
            print_button(screen,680,180,GRAY,TXT_SAVE)

    pygame.display.update()

pygame.quit()