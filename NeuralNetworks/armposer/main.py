"""Main Robo Arm file"""

import random
from operator import add
import copy
import pygame
from pygame.locals import *

from arm import *
from neuralnetwork import *
from saveload import *

SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

BLACK  = (000,000,000)
GREY   = (126,126,126)
WHITE  = (255,255,255)
RED    = (255,000,000)
GREEN  = (000,255,000)
BLUE   = (000,000,255)
YELLOW = (255,255,000)

def text(text,point,colour = WHITE):
    text_surface = font.render(str(text), False, colour)
    mainsurf.blit(text_surface, point)
    
def distance(p1,p2):
    return ((p1[0] - p2[0]) ** 2
            + (p1[1] - p2[1]) ** 2) ** 0.5

def drawline(points,
             colour = WHITE,
             width = 2):
    pygame.draw.lines(mainsurf,
                      colour,False,
                      points[0],
                      width)
    pygame.draw.lines(mainsurf,
                      colour,False,
                      points[1],
                      width)

def draw_species(arms, colours):
    for a, c in list(zip(arms, colours)):
        drawline(a.get_points(),c)

def draw_targets(target, colours):
    try:
        for t, c in list(zip(target, colours)):
            pygame.draw.circle(mainsurf, c, t, 4)
    except:
        print target
        a = 1/0
        
targets = (
    [410, 144],
    [659, 178],
    [162, 121],
    )

print targets
def target_cycle(target):
    for i in range(len(targets)):
        if distance(target, targets[i]) < 15:
            return list(
                map(
                    add,
                    targets[(i+1) % len(targets)],
                    [random.randint(-10,10),random.randint(-10,10)]
                    )
                )
        
##    return [random.randint(0,SURFACE_WIDTH),
##              random.randint(0,SURFACE_HEIGHT)]
    
# Simulation parameters
MUTATION_THRESHOLD = 0.2

MAX_DISTANCE = 10

# Initialization

### THESE ARE NEW GENERATION CONDITIONS!!! ###
inputs = (
       #"arm[i].Tangle['1']",
       #"arm[i].Tangle['2']",
       #"arm[i].Tangle['3']",
       "dist/float(MAX_DISTANCE)",
       "(olddist[i] - dist)",
       "2*arm[i].T['5'][0]/float(SURFACE_WIDTH)-1",
       "2*arm[i].T['5'][1]/float(SURFACE_HEIGHT)-1",
       "2*arm[i].T['4'][0]/float(SURFACE_WIDTH)-1",
       "2*arm[i].T['4'][1]/float(SURFACE_HEIGHT)-1",
       "2*arm[i].T['3'][0]/float(SURFACE_WIDTH)-1",
       "2*arm[i].T['3'][1]/float(SURFACE_HEIGHT)-1",
       "2*target[i][0]/float(SURFACE_WIDTH)-1",
       "2*target[i][1]/float(SURFACE_HEIGHT)-1",
       "2*target[i][0]/float(SURFACE_WIDTH)-1 - (2*arm[i].T['5'][0]/float(SURFACE_WIDTH)-1)",
       "2*target[i][1]/float(SURFACE_HEIGHT)-1 - (2*arm[i].T['5'][1]/float(SURFACE_HEIGHT)-1)"
       )
scorings = ("dist-1",
            "targetn[i]",
            "(dist - olddist[i])**3",
            "-arm[i].Tangle['1']**2",
            "-arm[i].Tangle['2']**2",
            "-arm[i].Tangle['3']**2",
            )
maxtime = 30
gencount = 0
mutationtimes = 3

gen = None
try:
    import os
    print 'Please, choose file to load (anything else to start over)'
    saves = list(enumerate(os.listdir('saves/')))
    for i, save in saves:
        print str(i)+' - '+save
    input_ = input()
    gen, inputs, scorings, gencount, maxtime = loadnet(saves[input_][1])
except (NameError, SyntaxError, IndexError):
    print 'Wrong filename'
    print 'Please, set max level'
    input_1 = input()
    print 'Please, set max nodes per level'
    input_2 = input()
    print 'Please, set generation size'
    input_3 = input()
    print """Please, choose activation fucntion:
0 - tangensoid
1 - sigmoid"""
    input_4 = input()
    gen = [Network(len(inputs),
                   3,
                   input_1,
                   input_2,
                   True,
                   bool(input_4)
                   ) for i in range(input_3)]
if len(gen) < 10:
    MUTATION_THRESHOLD = 0

     
arm = [Arm() for i in range(len(gen))]
colour = [(random.randint(20,255),
           random.randint(20,255),
           random.randint(20,255)
           ) for i in range(len(gen))]
target = [target_cycle(targets[-1]) for i in range(len(gen))]
screen = pygame.display.set_mode(
    (800, 600),
    HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Neural Net RoboArm Learner 3000')
mainsurf = pygame.Surface((SURFACE_WIDTH,
                          SURFACE_HEIGHT))
#clock = pygame.time.Clock()
FONT = 'Arial'
FONT_SIZE = 14
pygame.font.init()
font = pygame.font.SysFont(FONT, FONT_SIZE)

flag = {
    'run': True,
    'click': False,
    'targetchange': True,
    }

time = 0
olddist = [MAX_DISTANCE/float(1+distance(arm[i].T['5'],target[i])) for i in range(len(arm))]
score = [0 for i in range(len(gen))]
targetn = [0 for i in range(len(gen))]
while flag['run']:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag['run'] = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.size,
                HWSURFACE|DOUBLEBUF|RESIZABLE)
        elif event.type == MOUSEBUTTONDOWN:
            flag['click'] = True
            print pygame.mouse.get_pos()
        elif event.type == MOUSEBUTTONUP:
            flag['click'] = False
            
    # Arm calculation
    mainsurf.fill(BLACK)
    for i in range(len(arm)):
        dist = MAX_DISTANCE/float(1+distance(arm[i].T['5'],target[i]))
        
        ans = gen[i].run(
            [eval(inputs[j]) for j in range(len(inputs))]
            )
        arm[i].move_all(arm[i].Tangle['1'] + ans[0],
                        arm[i].Tangle['2'] + ans[1],
                        arm[i].Tangle['3'] + ans[2]
                        )
        
        for sc in scorings:
            score[i] = score[i] + eval(sc)
            
        #text(
            #score[i],
            #dist/float(MAX_DISTANCE),
            #2*arm[i].T['5'][0]/SURFACE_WIDTH-1,
            #dist,
            #arm[i].Tangle['1'],
            #arm[i].Tangle['2'],
            #arm[i].Tangle['3'],
            #arm[i].T['52'],colour[i])
        olddist[i] = dist
        
        if dist > float(MAX_DISTANCE)/10:
            target[i] = target_cycle(target[i])
            score[i] += MAX_DISTANCE
            targetn[i] += MAX_DISTANCE
    
    # Rendering
    text(time/float(maxtime),[0,0])
    draw_species(arm, colour)
    draw_targets(target, colour)
    screen.blit(pygame.transform.scale(mainsurf,screen.get_rect().size),(0,0))
    pygame.display.flip()
    #clock.tick(1)
    # Time calculations
    if time < maxtime:
        time += 1
    else:
        #for i in gen:
            #print i.control_sum()
        #print '\n'
        time = 0
        maxtime = min(300, maxtime + 5)
        for i in range(len(arm)):
            arm[i].set_default_pos()
            target[i] = target_cycle(targets[-1])
            targetn[i] = 0
        
        gen = [x for _, x in sorted(zip(score, gen), reverse = True)]
        colour = [x for _, x in sorted(zip(score, colour), reverse = True)]
        score.sort(reverse = True)

        nextgen = list()
        nextcolour = list()
        # Keeping top 10 % without modification
        times = 0
        for i in range(len(score)):
            times += 1
            if i/float(len(score)) >= MUTATION_THRESHOLD:
                break
            nextgen.append(copy.deepcopy(gen[i]))
            nextcolour.append(copy.deepcopy(colour[i]))
                
        # Appending with mutation
        while len(nextgen) < len(gen):
            i = proportional_pick(score)
            nextgen.append(copy.deepcopy(gen[i]))
            nextcolour.append(
                ((colour[i][0] + random.randint(-3,3))%235+20,
                 (colour[i][1] + random.randint(-3,3))%235+20,
                 (colour[i][2] + random.randint(-3,3))%235+20)
                )
            for i in range(mutationtimes):
                nextgen[-1].mutate()
            
        gen = copy.deepcopy(nextgen)
        colour = copy.deepcopy(nextcolour)
        score = [0 for i in range(len(gen))]
        gencount +=1
            
        #print gencount

pygame.quit()
savenet(gen, inputs, scorings, gencount, maxtime)
