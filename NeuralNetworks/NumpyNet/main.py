import numpy as np
import random
from copy import deepcopy
import pygame
from pygame.locals import *
from pgc import *

from ntw import Network
from arm import Arm


def drawline(points,
             colour,
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
    for t, c in list(zip(target, colours)):
        pygame.draw.circle(mainsurf, c, t, 4)

screen = pygame.display.set_mode(
    (800, 600),
    HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('NumPy neural network robotic handler 8000')
mainsurf = pygame.Surface((SURFACE_WIDTH,
                          SURFACE_HEIGHT))

NOT_MUTATED_IN_CHILDREN = 10

species = 1000
hlayers = 1


net    = [Network() for i in range(species)]
arm    = [Arm() for i in range(species)]
color  = [WHITE for i in range(species)]
score  = np.array([0.0 for i in range(species)])
target = [np.array([600, 200]) for i in range(species)]

time = 0
lifetime = 100
for i in range(species):
    for j in range(hlayers):
        net[i].mutate(1)
        net[i].mutate(0)
    color[i] = (random.randrange(256),
                random.randrange(256),
                random.randrange(256))

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    mainsurf.fill(BLACK)
    draw_species(arm, color)
    draw_targets(target, color)
    
    # Logic for arms
    for i in range(species):
        inputv = np.array(arm[i].get_angles())
        output = net[i].run(inputv)
        arm[i].move_all(output)
        dist = arm[i].T['5'] - target[i]
        score[i] += 10000 / (1 + dist.dot(dist))# - 1
        if time % 10 == 0:
                # Best will be green, worse - red
                color_k = 510 / (max(score) + min(score))
                color_red = max(min(255, -color_k * score[i] + color_k * max(score)), 0)
                color_green = max(min(255,  color_k * score[i] + color_k * min(score)), 0)
                #color_blue = min(color_red, color_green)
                color[i] = (color_red, color_green, 0)#color_blue)

    time +=1
   
    # Restart
    if time > lifetime:
    	# Print max score
    	print(max(score))
    
    	# New generation compilation
    	scoresortedindecies = np.flip(np.argsort(score))
    	
    	#net[scoresortedindecies[0]].show()
    	
    	newnet = []
    	for i in range(NOT_MUTATED_IN_CHILDREN):
    	    newnet.append(net[scoresortedindecies[i]])
    	
    	for i in range(NOT_MUTATED_IN_CHILDREN, species):
    	    newnet.append(deepcopy(newnet[random.randrange(NOT_MUTATED_IN_CHILDREN)]))
    	    newnet[-1].mutate()
    	
    	net = newnet
    	#net[0].show()
    	
    	# Simulation restart
    	#if lifetime < 200:
	
    	    	#lifetime += 1
		
    	time = 0
	
    	for i in range(species):
    	    	arm[i].set_default_pos()
    	    	score[i] = 0
    	 	
    	print()
        
    # Frame Render    
    screen.blit(pygame.transform.scale(mainsurf,screen.get_rect().size),(0,0))
    pygame.display.flip()

pygame.quit()
