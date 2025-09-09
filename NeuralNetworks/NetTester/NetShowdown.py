#Neural Network drawer

#




import pygame
from pygame.locals import *

from perceptrones import *
import random

from copy import copy

WIDTH = 800
HEIGHT = 600
FONT = 'Arial'
FONT_SIZE = 14

stdRad = 13

pygame.init()
 
pygame.font.init()
font = pygame.font.SysFont(FONT, FONT_SIZE)
real_screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
screen = real_screen.copy()
pygame.display.set_caption('Neural Net Showdown')
#clock = pygame.time.Clock()

def joint(x, rad, colour):
        
    pygame.draw.circle(screen, colour, [x[0],x[1]], rad)
    pygame.draw.circle(screen, BLACK, [x[0],x[1]], rad-2)
    
def jointoutline(x, rad, colour):
        
    pygame.draw.circle(screen, colour, [x[0],x[1]], rad)
    pygame.draw.circle(screen, BLACK, [x[0],x[1]], rad-1)
    
def text(text,point,colour = WHITE):
    text_surface = font.render(str(text), False, colour)
    screen.blit(text_surface, point)

def draw_political_coordinates():
    pygame.draw.line(screen, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    pygame.draw.line(screen, WHITE, (0,  HEIGHT/2),(WIDTH, HEIGHT/2))

def draw_link(xy1,xy2,weight,colour = None):
    if colour == None:
        colour = (min(int(-(weight)*255+255),255),
                int(255-255*abs(weight)),
                min(int((weight+1)*255),255))
    pygame.draw.line(screen, colour, xy1, xy2)
    text(weight,
         (xy1[0]/2+xy2[0]/2,xy1[1]/2+xy2[1]/2-16),
         colour)
    
def GetNetwork(filename = ''):
    
    net = Network()
    if filename != '':
        with open('saves/'+filename) as f:
          i = -1
          flag = False
          for line in f:
            if line[line.find('\t'):line.rfind('\t')] == '\t[]': #True if output neuron
              flag = True
              continue
            elif flag:
              flag = False
              i+= 1
              
            temp = list()
            
            if line != '\n':
              #get [[a, wa], [b, wb], ... [z, wz]]
              slinks = line[line.find('\t')+1:line.rfind('\t')-1]
              
              newlinks = list()

              ifrom = 1
              while ifrom < len(slinks)-1:

                temp.append([int(slinks[slinks.find('[',ifrom)+1:slinks.find(',',ifrom)]),
                               float(slinks[slinks.find(',',ifrom)+2:slinks.find(']',ifrom)])])
                
                ifrom = slinks.find(']',ifrom)+2
              #temp is slinks but in adequate list form

              #Add node to certain lvl
              if line[line.rfind('\t')+1:-1] != '0': #If not input neuron
                #print i,int(line[line.rfind('\t')+1:-1])
                net.AddNode(int(line[line.rfind('\t')+1:-1]))
                
            net.node[int(line[:line.find('\t')])].links = temp
        
    return net

def Save(net, name = 'ShowdownNet'):
    import datetime
    filename = 'saves/'+name+str(datetime.datetime.now()).replace(':','')+'.txt'
    with open(filename,'w') as f:
        for i in range(len(net.node)):
            f.write(str(i)+'\t'+str(net.node[i].links)+'\t'
                  +str(net.node[i].level)+'\n')
            
net = GetNetwork()#'Show.txt')


#allowed_coordinated[lvl][n]
allowed_coordinates = list() #0: n, [x,y]; n2, [x2, y2]
                             #1: n, [x,y]; ...
for lvl in range(MAX_LEVEL+1):
    allowed_coordinates.append(list())
    for n in range(MAX_NODES_PER_LEVEL):
        allowed_coordinates[lvl].append([WIDTH/(MAX_LEVEL+2)*lvl+WIDTH/(MAX_LEVEL+2),
                          HEIGHT/(MAX_NODES_PER_LEVEL+2)*n+HEIGHT/(MAX_NODES_PER_LEVEL+2)*1.5])




RUNNING = True
click = False
edit = False
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False 
        elif event.type == VIDEORESIZE:
            real_screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            click = False
            
    screen.fill(BLACK)
    #draw_political_coordinates()


    inp = pygame.mouse.get_pos()
    inp = [float(inp[0]) / WIDTH, float(inp[1]) / HEIGHT]
    ans = net.Run(inp)
    joint((ans[0]*WIDTH,ans[1]*HEIGHT),3,GREEN)
    #Draw nodes

    #Draw possible positions for nodes
    cursor = pygame.mouse.get_pos()
    cursored = -1
    for x in allowed_coordinates:
        for xy in x:                    
            jointoutline(xy,stdRad,GREY)

    #Mutation button

    if cursor[0] + cursor[1] > HEIGHT + WIDTH - 30:
        pygame.draw.polygon(screen, RED,
                            [(WIDTH,HEIGHT),(WIDTH-30,HEIGHT),(WIDTH,HEIGHT-30)]
                            )
        if click:
            net.Mutate()
            click = False
            net.Run(inp)
    
    elif cursor[0] + cursor[1] < 30:
        pygame.draw.polygon(screen, BLUE,
                            [(0,0),(30,0),(0,30)]
                            )
        if click:
            edit = not edit

    #Assign nodes
    taken = [0 for i in range(MAX_LEVEL+1)]
    nodesxys = list()
    for node in net.node:
        #joint(allowed_coordinates[node.level][taken[node.level]],stdRad,WHITE)
        nodesxys.append(allowed_coordinates[node.level][taken[node.level]])
        taken[node.level] += 1
        if abs(cursor[0]-nodesxys[-1][0])+abs(cursor[1]-nodesxys[-1][1]) < 15:
            cursored = len(nodesxys)-1
    
    
    if cursored != -1:        
        for i in range(len(net.node)):
            for link in net.node[i].links:
                if i == cursored or link[0] == cursored:
                    draw_link(nodesxys[i],nodesxys[link[0]],link[1])
                    joint(nodesxys[i],stdRad,WHITE)
                    if i < 10 and click:
                        text('0'+str(i),
                         (nodesxys[i][0]-6,nodesxys[i][1]-8),
                         YELLOW)
                    elif click:
                        text(i,
                         (nodesxys[i][0]-6,nodesxys[i][1]-8),
                         YELLOW)
                    text(net.node[i].signal,(nodesxys[i][0]-20,nodesxys[i][1]),CYAN)
                    joint(nodesxys[link[0]],stdRad,WHITE)
                    if link[0] < 10 and click:
                        text('0'+str(link[0]),
                         (nodesxys[link[0]][0]-6,nodesxys[link[0]][1]-8),
                         YELLOW)
                    elif click:
                        text(link[0],
                         (nodesxys[link[0]][0]-6,nodesxys[link[0]][1]-8),
                         YELLOW)
                    text(net.node[link[0]].signal,(nodesxys[link[0]][0]-20,nodesxys[link[0]][1]),CYAN)
                    
        
    else:
        
        #Draw lines
        for i in range(len(net.node)):
            for link in net.node[i].links:
                draw_link(nodesxys[i],nodesxys[link[0]],link[1])
                
        #Draw nodes
        for i in range(len(net.node)):
            joint(nodesxys[i],stdRad,WHITE)
            if i < 10 and click:
                text('0'+str(i),
                 (nodesxys[i][0]-6,nodesxys[i][1]-8),
                 YELLOW)
            elif click:
                text(i,
                 (nodesxys[i][0]-6,nodesxys[i][1]-8),
                 YELLOW)

        #Inputs-outputs cycle perhaps
        for i in range(net.LvlQ(MAX_LEVEL)): #Outputs
            text(net.node[i].signal,(nodesxys[i][0]-20,nodesxys[i][1]),CYAN)

        for i in range(net.LvlQ(MAX_LEVEL),net.LvlQ(0)+net.LvlQ(MAX_LEVEL)): #Inputs
            text(net.node[i].signal,(nodesxys[i][0]-20,nodesxys[i][1]),CYAN)

        for i in range(net.LvlQ(0)+net.LvlQ(MAX_LEVEL),len(net.node)): #Hiddens
            text(net.node[i].signal,(nodesxys[i][0]-20,nodesxys[i][1]),CYAN)

    real_screen.blit(pygame.transform.scale(
        screen, real_screen.get_rect().size),
                     (0, 0))
    pygame.display.flip()
    
Save(net)
pygame.quit()






