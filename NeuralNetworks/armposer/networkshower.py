import os
from random import npercent

import pygame
from pygame.locals import *

from neuralnetwork import *
from neuralnetwork import _MAX_WEIGHT
from saveload import *
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

FONT = 'Times New Roman'
FONT_SIZE = 14

BLACK  = (000,000,000)
GREY   = (126,126,126)
WHITE  = (255,255,255)
RED    = (255,000,000)
GREEN  = (000,255,000)
BLUE   = (000,000,255)
YELLOW = (255,255,000)

def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def draw_node(point,
           radius,
           color = WHITE,
           hollow = True,
           bias_weight = None,
           width = 2):
    pygame.draw.circle(mainsurf,
                       color,
                       point,
                       radius)
    if hollow:
        pygame.draw.circle(mainsurf,
                           BLACK,
                           point,
                           radius - width)
    if bias_weight is not None:
        text(bias_weight, [point[0]-10,point[1]+7], color)
        
def draw_link(point1,
              point2,
              weight):
    
    color = (
        min(int(-(weight / _MAX_WEIGHT)*255+255),255),
        int(255-255*abs(weight / _MAX_WEIGHT)),
        min(int((weight / _MAX_WEIGHT+1)*255),255)
             )
    pygame.draw.line(
        mainsurf,
        color,
        point1,
        point2,
        1
        )
    text(
        weight,
        [point1[0]/2.0+point2[0]/2.0,
         point1[1]/2.0+point2[1]/2.0],
        color
        )
         
def text(text,point,colour = WHITE):
    text_surface = font.render(str(text), False, colour)
    mainsurf.blit(text_surface, point)
    
def get_wh(net):
    n = len(net.node)
    dw = 30
    widthes = range(
        (SURFACE_WIDTH-dw)/(n+1)+dw/3,
        (SURFACE_WIDTH-dw)-dw/3*2,
        ((SURFACE_WIDTH-dw) - (SURFACE_WIDTH-dw)/(n+1))/n
        )
    if len(widthes) > n:
        widthes.pop()
        
    heights = list()
    for lvl in range(len(net.node)):
        n = len(net.node[lvl])
        if n == 0:
            heights.append([])
            continue
        heights.append(
            range(
                SURFACE_HEIGHT/(n+1),
                SURFACE_HEIGHT,
                (SURFACE_HEIGHT - SURFACE_HEIGHT/(n+1))/n
                )
            )
        if len(heights[-1]) > n:
            heights[-1].pop()
    return widthes, heights

def get_cursored(mousepoint):
    
    for lvl in range(len(gen[g].node)):
        for n in range(len(gen[g].node[lvl])):
            if distance(
                mousepoint,
                [widthes[lvl],
                 heights[lvl][n]]
                ) < 10:
                return lvl, n
    return -1, -1

print 'Please, choose file to load'
saves = list(enumerate(os.listdir('saves/')))
for i, save in saves:
    print str(i)+' - '+save
input_ = input()
while input_ > len(saves) or type(input_) is not int:
    print 'Please, choose file to load'
    input_ = input()
print saves[input_][1]
gen = loadnet(saves[input_][1])[0]
        
screen = pygame.display.set_mode(
    (800, 600),
    HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Neural Net Showdown 3')
mainsurf = pygame.Surface((SURFACE_WIDTH,
                          SURFACE_HEIGHT))
pygame.font.init()
font = pygame.font.SysFont(FONT, FONT_SIZE)

flag = {
    'run': True,
    'click': False,
    'inputcycle': False,
    'mutate': False
    }

class Slider():
    
    def __init__(self,
                 minvalue,
                 maxvalue,
                 point1,
                 point2,
                 vertical = True):
        self.vertical = vertical
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.point1 = point1
        self.point2 = point2
        self.value = (self.minvalue+self.maxvalue)/2.0
        self.point = [
            (self.point1[i]+self.point2[i])/2.0 for i in range(2)]

    def set_value(self):                         
        self.value = (self.point[int(self.vertical)]
                      - self.point2[int(self.vertical)]
                      ) * (
                          self.maxvalue
                          - self.minvalue
                          ) / float(
                              self.point1[int(self.vertical)]
                              -self.point2[int(self.vertical)]
                              ) + self.minvalue
        
    def move_to(self, pointto):
        self.point = [min(self.point2[i],
                         max(self.point1[i],
                             pointto[i])) for i in range(2)]
        self.set_value()
        
    def move_to_output(self,valueto):
        self.value = valueto
        self.point[1] = (self.value
                         -self.minvalue
                         ) * (
                             self.point1[1]
                             -self.point2[1]
                             ) / float(
                                 self.maxvalue
                                 -self.minvalue
                                 ) + self.point2[1]
        
    def draw(self,hollow = True,dx = 30):
        pygame.draw.line(
            mainsurf,
            WHITE,
            self.point1,
            self.point2,
            1
        )
        draw_node(self.point,
           3,YELLOW,
           hollow,
           width = 2)
        text(self.value,
             [self.point1[0] - dx,
              (self.point1[1] + self.point2[1]) / 2]
             )

        
g = 0
widthes, heights = get_wh(gen[g])
#print widthes

dx = 30
dy2 = 20
inputs = [Slider(-1,
                 1,
                 [widthes[0] - dx,
                  heights[0][n] - dy2],
                 [widthes[0] - dx,
                  heights[0][n] + dy2]) for n in range(len(gen[g].node[0]))
          ]

outputs = [Slider(-1,
                 1,
                 [widthes[-1] + dx,
                  heights[-1][n] - dy2],
                 [widthes[-1] + dx,
                  heights[-1][n] + dy2]) for n in range(len(gen[g].node[-1]))
          ]

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
            #print pygame.mouse.get_pos()
        elif event.type == MOUSEBUTTONUP:
            flag['click'] = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                g = max(0,
                        g-1)
            elif event.key == pygame.K_RIGHT:
                g = min(len(gen)-1,
                        g+1)
            elif event.key == pygame.K_UP:
                for i in range(100):
                    gen[g].mutate()
            elif event.key == pygame.K_DOWN:
                flag['inputcycle'] = not flag['inputcycle']
            widthes, heights = get_wh(gen[g])
                    
    mainsurf.fill(BLACK)
    text(g, [SURFACE_WIDTH/2, 10])
    curpos = pygame.mouse.get_pos()
    cursorlvl, cursorn = get_cursored(curpos)
    for sl in inputs:
        if flag['inputcycle']:
            sl.value = npercent()
        if distance(sl.point,curpos) < 15 and flag['click']:
            sl.move_to(curpos)
            sl.draw(False)
        else:
            sl.draw()
    gen[g].run([sl.value for sl in inputs])
    for i in range(len(outputs)):
        if distance(outputs[i].point,curpos) < 15 and flag['click']:
            flag['click'] = False
            gen[g].mutate()
        outputs[i].move_to_output(gen[g].node[-1][i].signal)
        outputs[i].draw(dx = -15)
        
    if (cursorlvl == -1):
        for lvl in range(len(gen[g].node)):
            for n in range(len(gen[g].node[lvl])):
                draw_node(
                    [widthes[lvl],
                     heights[lvl][n]
                     ],
                    10,
                    WHITE,
                    True,
                    gen[g].node[lvl][n].bias_weight)
                for link in gen[g].node[lvl][n].links:
                    draw_link(
                        [widthes[lvl],
                         heights[lvl][n]],
                        [widthes[link[0]],
                         heights[link[0]][link[1]]],
                        link[2]
                        )
    else:
        draw_node(
            [widthes[cursorlvl],
             heights[cursorlvl][cursorn]
             ],
            10,
            WHITE,
            True,
            gen[g].node[lvl][n].bias_weight)
        for link in gen[g].node[cursorlvl][cursorn].links:
            draw_node(
                [widthes[link[0]],
                 heights[link[0]][link[1]]
                 ],
                10,
                WHITE,
                True,
                gen[g].node[lvl][n].bias_weight)
            draw_link(
                [widthes[cursorlvl],
                 heights[cursorlvl][cursorn]],
                [widthes[link[0]],
                 heights[link[0]][link[1]]],
                link[2]
                )

    screen.blit(
        pygame.transform.scale(
            mainsurf,screen.get_rect().size
            ),
        (0,0)
        )
    pygame.display.flip()

pygame.quit()
