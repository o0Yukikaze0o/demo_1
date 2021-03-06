import pygame
import time
from components import Histogram
from demoPlayer import Player, RandomNote

MIDI_FILE_NAME = "(Nozomi Tenma) Clannad - _Shining in the Sky_.mid"
OUTPUT_FILE_NAME = "out.mid"
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
TXT_CLEAR = defaultFont.render('CLEAR',True,BLACK)
TXT_WARN = defaultFont.render('MISSING PIANO TRACK!!',True,BLACK)

def print_button(screen,x,y,color,text):
    pygame.draw.rect(screen,color,[x,y,100,60])
    screen.blit(text,(x+5,y+10))

screen.fill(BLUE)
print_button(screen,680,20,GRAY,TXT_PLAY)
print_button(screen,680,100,GRAY,TXT_RANDOM)
print_button(screen,680,180,GRAY,TXT_SAVE)
print_button(screen,560,180,GRAY,TXT_CLEAR)
running = True

def print_bar(screen,now,max,hist):
    # print the progress bar
    pygame.draw.rect(screen,GRAY,[0,260,800,20])
    pygame.draw.rect(screen,GREEN,[0,260,800*now/max,20])
    # print the histogram bar
    pygame.draw.rect(screen,BLUE,[0,280,800,320])
    for i in range(len(hist.hist)):
        height = int(1 + 299 * hist.hist[i] / hist.max)
        pygame.draw.rect(screen,RED,[5+6*i,590-height,4,height])

# open the MIDI file
pygame.midi.init()
device = pygame.midi.Output(1)
player1 = Player(MIDI_FILE_NAME,device)
if not player1.track: # missing piano
    running = False
    screen.fill(RED)
    screen.blit(TXT_WARN,(250,290))
    time.sleep(5)
else:
    hist = Histogram(player1.deltaTime)
    print_bar(screen,0,player1.maxTick,hist)
pygame.display.update()
randNote = RandomNote(OUTPUT_FILE_NAME,player1.deltaTime,device)
# main loop
while running:
    # handle different events
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
                player1.update()
            elif 680 <= mouse[0] < 780 and 100 <= mouse[1] < 160:
                print_button(screen,680,100,GREEN,TXT_RANDOM)
                if player1.isPlaying:
                    player1.update()
                i, p = hist.top10()
                randNote.read(i,p)
                randNote.generate()
                randNote.play()
            elif 680 <= mouse[0] < 780 and 180 <= mouse[1] < 240:
                print_button(screen,680,180,GREEN,TXT_SAVE)
                randNote.save()
            elif 560 <= mouse[0] < 660 and 180 <= mouse[1] < 240:
                print_button(screen,560,180,GREEN,TXT_CLEAR)
                if player1.isPlaying:
                    player1.update()
                hist.clearAll()
                print_bar(screen,player1.nextTick,player1.maxTick,hist)
            elif 260 <= mouse[1] < 280:
                player1.nextTick = int(player1.maxTick * mouse[0] / 800)
                player1.update(False)
                hist.clearActive()
                print_bar(screen,player1.nextTick,player1.maxTick,hist)
        elif event.type == pygame.MOUSEBUTTONUP:
            print_button(screen,680,20,GRAY,TXT_PLAY)
            print_button(screen,680,100,GRAY,TXT_RANDOM)
            print_button(screen,680,180,GRAY,TXT_SAVE)
            print_button(screen,560,180,GRAY,TXT_CLEAR)

    # music player
    if player1.isPlaying:
        msg = player1.playNextMessage(time.time())
        if msg:
            hist.new_note(msg)
        print_bar(screen,player1.nextTick,player1.maxTick,hist)

    pygame.display.update()

pygame.quit()