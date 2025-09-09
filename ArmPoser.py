#This one is from pypose
import pygame
from math import cos
from math import sin
import cmath

from ax12 import *
from MNK import *
from operator import add

# Uncomment and f5 to get coefficients for free :D
##coef = CoefGet()
##psi = 0.246441600965
##pi = 3.1415926535897
##pi2 = pi/2
##linear_k = dict()
##linear_b = dict()
##MAX_POS = dict()
##MIN_POS = dict()
##linear_k['1'], linear_b['1'] = MNK(
##    [coef[82],coef[83],coef[84],coef[85],coef[86]],
##                     [coef[87]/57.29578+psi,
##                      coef[88]/57.29578+psi,
##                      coef[89]/57.29578+psi,
##                      coef[90]/57.29578+psi,
##                      coef[91]/57.29578+psi])
##
##linear_k['2'], linear_b['2'] = MNK(
##    [coef[92],coef[93],coef[94],coef[95],coef[96]],
##                     [coef[97]/57.29578,
##                      coef[98]/57.29578,
##                      coef[99]/57.29578,
##                      coef[100]/57.29578,
##                      coef[101]/57.29578])
##
##linear_k['3'], linear_b['3'] = MNK(
##    [coef[102],coef[103],coef[104],coef[105],coef[106]],
##                     [coef[107]/57.29578,
##                      coef[108]/57.29578,
##                      coef[109]/57.29578,
##                      coef[110]/57.29578,
##                      coef[111]/57.29578])
##    
##linear_k['0s'], linear_b['0s'] = MNK(
##    [coef[72],coef[73],coef[74],coef[75],coef[76]],
##                     [coef[77]/57.29578,
##                      coef[78]/57.29578,
##                      coef[79]/57.29578,
##                      coef[80]/57.29578,
##                      coef[81]/57.29578])
##
##linear_k['7'], linear_b['7'] = MNK(
##    [coef[112],coef[113],coef[114],coef[115],coef[116]],
##                     [coef[117]/57.29578,
##                      coef[118]/57.29578,
##                      coef[119]/57.29578,
##                      coef[120]/57.29578,
##                      coef[121]/57.29578])
##
##linear_k['8'], linear_b['8'] = MNK(
##    [coef[122],coef[123],coef[124],coef[125],coef[126]],
##                     [coef[127]/57.29578,
##                      coef[128]/57.29578,
##                      coef[129]/57.29578,
##                      coef[130]/57.29578,
##                      coef[131]/57.29578])
##
##MIN_POS = {
##    '1': coef[82],
##    '2': coef[92],
##    '3': coef[102],
##    '0s': coef[72],
##    '7': coef[112],
##    '8': coef[122]
##    }
##
##MAX_POS = {
##    '1': coef[86],
##    '2': coef[96],
##    '3': coef[106],
##    '0s': coef[76],
##    '7': coef[116],
##    '8': coef[126]
##    }
##print('k:',linear_k)
##print('b:',linear_b)
##print('min:',MIN_POS)
##print('max:',MAX_POS)
##
##a = 1/0

#Essentials
def ArmPoser(port):
    
    #Constants

    #Fundamentals
    
    pi = 3.1415926535897
    pi2 = pi/2
    
    #Colours
    BLACK  = (000, 000, 000)
    RED    = (255, 000, 000)
    GREEN  = (000, 255, 000)
    BLUE   = (000, 000, 255)
    YELLOW = (255, 255, 000)
    CYAN   = (000, 255, 255)
    PURPLE = (255, 000, 255)
    WHITE  = (255, 255, 255)

    DARKRED    = (128, 000, 000)
    DARKGREEN  = (000, 128, 000)
    DARKBLUE   = (000, 000, 128)
    ORANGE     = (255, 128, 000)
    DARKCYAN   = (000, 128, 128)
    VIOLET     = (128, 000, 128)
    GREY       = (128, 128, 128)

    PINK = (255, 128, 128)
    
    # Window properties
    WINDOW_NAME = 'Arm Poser 2000'

    WIDTH = 1000
    HEIGHT = 600

    FONT = 'Times New Roman'
    FONT_SIZE = 14

    #Axes
    AXES_SHIFT = 30
    BSTEP = 50
    BSIZE = 5
    JRAD = 6

    A0 = [AXES_SHIFT,
          HEIGHT - AXES_SHIFT]
    Az = [AXES_SHIFT,
          AXES_SHIFT]
    Ar = [WIDTH - AXES_SHIFT,
          HEIGHT - AXES_SHIFT]
    Am = [WIDTH - AXES_SHIFT,
          AXES_SHIFT]

    roSHIFT = -350
    zSHIFT = 0
    jointSHIFT = [-20,-15]
    modesSHIFT = [15,-8]
    sliderSHIFT = [-8,8]

    # Real coefficients
    coef = CoefGet()
    
    #Arm dimensions
    f0 = coef[148]      # Pedestal height
    d0 = coef[142]     # Pedestal length
    f05 = coef[149]  # Pedestal-joint height

    d1 = coef[140]   # Triangle length
    f1 = coef[141]    # Triangle height
    c1 = coef[143]  # Triangle hypotenuse
    psi = 0.246441600965

    d2 = coef[144]   # Elbow length

    d3 = coef[145]  # Wrist length

    d4 = coef[146]      # Claw length
    f4 = coef[147]    # Claw height

    l1 = 38.4
    l15 = 69
    h15 = 25.7
    h1 = 172.5

    #Pos - IRL dependence
    # y = ki * x + bi   <=> IRL = ki * pos + bi
    # x = (y - bi) / ki <=> pos = (IRL - bi) / ki
    
    linear_k = {
        '1': 0.005018518573309175,
        '2': 0.005094898222254254,
        '3': -0.0051528193983891,
        '0s': 1,
        '7': 1,
        '8': 30.35
        }
    linear_b = {
        '1': -2.287910278556134,
        '2': -1.2725488098199669,
        '3': 3.4681186561368325,
        '0s': 1,
        '7': 1,
        '8': 1.3
        }
    
    linear_k['1'], linear_b['1'] = MNK(
        [coef[82],coef[83],coef[84],coef[85],coef[86]],
                         [coef[87]/57.29578+psi,
                          coef[88]/57.29578+psi,
                          coef[89]/57.29578+psi,
                          coef[90]/57.29578+psi,
                          coef[91]/57.29578+psi])
    
    linear_k['2'], linear_b['2'] = MNK(
        [coef[92],coef[93],coef[94],coef[95],coef[96]],
                         [coef[97]/57.29578,
                          coef[98]/57.29578,
                          coef[99]/57.29578,
                          coef[100]/57.29578,
                          coef[101]/57.29578])
    
    linear_k['3'], linear_b['3'] = MNK(
        [coef[102],coef[103],coef[104],coef[105],coef[106]],
                         [coef[107]/57.29578,
                          coef[108]/57.29578,
                          coef[109]/57.29578,
                          coef[110]/57.29578,
                          coef[111]/57.29578])
        
    linear_k['0s'], linear_b['0s'] = MNK(
        [coef[72],coef[73],coef[74],coef[75],coef[76]],
                         [coef[77]/57.29578,
                          coef[78]/57.29578,
                          coef[79]/57.29578,
                          coef[80]/57.29578,
                          coef[81]/57.29578])

    linear_k['7'], linear_b['7'] = MNK(
        [coef[112],coef[113],coef[114],coef[115],coef[116]],
                         [coef[117]/57.29578,
                          coef[118]/57.29578,
                          coef[119]/57.29578,
                          coef[120]/57.29578,
                          coef[121]/57.29578])

    linear_k['8'], linear_b['8'] = MNK(
        [coef[122],coef[123],coef[124],coef[125],coef[126]],
                         [coef[127]/57.29578,
                          coef[128]/57.29578,
                          coef[129]/57.29578,
                          coef[130]/57.29578,
                          coef[131]/57.29578])
    
    MIN_POS = {
        '1': coef[82],
        '2': coef[92],
        '3': coef[102],
        '0s': coef[72],
        '7': coef[112],
        '8': coef[122]
        }

    MAX_POS = {
        '1': coef[86],
        '2': coef[96],
        '3': coef[106],
        '0s': coef[76],
        '7': coef[116],
        '8': coef[126]
        }
    #Points
    T = {
         'm': [0, 0],
         'amode': [65, 34],
         'smode': [65, 54],
         'speed': [65, 74],
         'exit': [WIDTH - 50, 40],
         'limits': [65, 94],
         'live': [65, 114],
         'rainbow': [65, 134]
         }
    pcolour = {
        '0': RED,
        '1': RED,
        '2': BLUE,
        '3': BLUE,
        '4': BLUE,
        '0s': PINK,
        '7': PINK,
        '8': PINK,
        'amode': GREEN,
        'smode': GREEN,
        'speed': CYAN,
        'exit': RED,
        'limits': CYAN,
        'live': GREEN,
        'rainbow': (255,0,0) 
        }

    #Angles
    Tangle = {
        '1': -1.32154,
        '2':  2.88878,
        '3':  0.25896
        } 

    psize = {
        '0': JRAD,
        '1': JRAD,
        '2': JRAD,
        '3': JRAD,
        '4': JRAD,
        '0s': JRAD - 2,
        '7': JRAD - 2,
        '8': JRAD - 2,
        'amode': JRAD,
        'smode': JRAD,
        'speed': JRAD,
        'exit': JRAD,
        'limits': JRAD,
        'live': JRAD,
        'rainbow': JRAD 
        }
        
    slider = {
        '0s': 0.5,
        '7': 0.5,
        '8': 0.7
        }


    #Flags
    MODES = {
        'amode': 'pos',
        'smode': 'pos',
        'speed': 10,
        'exit': True,
        'limits': True,
        'live': False,
        'rainbow': False
        }
    MPRESS = False

    hover = 'm'
    rainbowcount = 0
    length0 = 150
    length7 = 45
    length8 = 30
    rotators_dist = 1.75

    #Functions
    def text(text,point,colour = WHITE):
        text_surface = font.render(str(text), False, colour)
        screen.blit(text_surface, point)

    def ctext(*texd):
        tex = ''
        for n in texd:
            tex += str(n)
        text(tex,list(map(add,T['m'],[5,-5])))
        
    def axes_draw(colour = WHITE):
        
        pygame.draw.line(screen, colour, A0, Ar, 2) #ro axis
        pygame.draw.line(screen, colour, A0, Az, 2) #z axis

        x = A0[0]; y = A0[1]
        while x < Ar[0]:
            pygame.draw.line(screen, colour, [x, y], [x, y - BSIZE], 1)
            text(str(x), [x, y + FONT_SIZE//2] )
            x += BSTEP

        text('ro',[Ar[0], Ar[1] + FONT_SIZE//2])
        
        x = A0[0]; y = A0[1]
        while y > Az[1]:
            pygame.draw.line(screen, colour, [x, y], [x + BSIZE, y], 1)
            text(str(y), [x - 2 * FONT_SIZE, y])
            y -= BSTEP
        
        text('z', [Az[0] - FONT_SIZE, Az[1]])

    def get_pos():
        
        if port != None:
            p1 = port.getReg(1,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            slider['0s'] = (p1-MIN_POS['0s'])/(MAX_POS['0s']-MIN_POS['0s'])
            p1 = port.getReg(2,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            Tangle['1'] = p1*linear_k['1']+linear_b['1']
            p1 = port.getReg(5,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            Tangle['2'] = p1*linear_k['2']+linear_b['2']
            p1 = port.getReg(6,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            Tangle['3'] = p1*linear_k['3']+linear_b['3']
            p1 = port.getReg(7,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            slider['7'] = (p1-MIN_POS['7'])/(MAX_POS['7']-MIN_POS['7'])
            p1 = port.getReg(8,P_PRESENT_POSITION_L, 2)
            if p1 == -1:
                p1 = [0,2]
            p1 = p1[0]+p1[1]*256
            slider['8'] = (p1-MIN_POS['8'])/(MAX_POS['8']-MIN_POS['8'])
        else:
            print('no port open lol')

    def calculate_arm():
        T['0']  = [380,
                   570]
        T['01'] = [T['0'][0] - d0/2,
                   T['0'][1]       ]
        T['02'] = [T['0'][0] - d0/2,
                   T['0'][1] - f0  ]
        T['03'] = [T['0'][0] + d0/2,
                   T['0'][1] - f0  ]
        T['04'] = [T['0'][0] + d0/2,
                   T['0'][1]       ]
        T['1']  = [T['0'][0]           ,
                   T['0'][1] - f0 - f05]
        T['2']  = [T['1'][0] + c1 * cos(Tangle['1'] - pi2),
                   T['1'][1] + c1 * sin(Tangle['1'] - pi2)]
        T['15'] = [T['1'][0] + d1 * cos(Tangle['1'] - psi - pi2),
                   T['1'][1] + d1 * sin(Tangle['1'] - psi - pi2)]
        T['3']  = [T['2'][0] + d2 * cos(Tangle['1'] + Tangle['2'] - pi2),
                   T['2'][1] + d2 * sin(Tangle['1'] + Tangle['2'] - pi2)]
        T['4']  = [T['3'][0] + d3 * cos(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi2),
                   T['3'][1] + d3 * sin(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi2)]
        T['5']  = [T['3'][0] + (d3+d4/2) * cos(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi2),
                   T['3'][1] + (d3+d4/2) * sin(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi2)]
        T['51'] = [T['4'][0] + f4/2 * cos(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi),
                   T['4'][1] + f4/2 * sin(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi)]
        T['52'] = [T['51'][0] + d4 * cos(Tangle['1'] + Tangle['2'] + Tangle['3'] - pi2),
                   T['51'][1] + d4 * sin(Tangle['1'] + Tangle['2'] + Tangle['3']- pi2)]
        T['53'] = [T['52'][0] + f4 * cos(Tangle['1'] + Tangle['2'] + Tangle['3']),
                   T['52'][1] + f4 * sin(Tangle['1'] + Tangle['2'] + Tangle['3'])]
        T['54'] = [T['53'][0] + d4 * cos(Tangle['1'] + Tangle['2'] + Tangle['3'] + pi2),
                   T['53'][1] + d4 * sin(Tangle['1'] + Tangle['2'] + Tangle['3'] + pi2)]
        T['0smax'] = [T['1'][0] + length0/2         ,
                      T['1'][1] + f4 * rotators_dist]
        T['0smin'] = [T['0smax'][0] - length0,
                     T['0smax'][1]          ]
        T['7max'] = [T['4'][0] + length7/2         ,
                     T['4'][1] + f4 * rotators_dist]
        T['7min'] = [T['7max'][0] - length7,
                     T['7max'][1]          ]
        T['8max'] = [T['4'][0] + f4 * rotators_dist,
                     T['4'][1] + length8/2         ]
        T['8min'] = [T['8max'][0]          ,
                     T['8max'][1] - length8]
        T['0s'] = [T['0smin'][0] * (1 - slider['0s']) + T['0smax'][0] * slider['0s'],
                   T['0smin'][1]                                                ]
        T['7'] = [T['7min'][0] * (1 - slider['7']) + T['7max'][0] * slider['7'],
                  T['7min'][1]                                                 ]
        T['8'] = [T['8min'][0]                                                 ,
                  T['8min'][1] * slider['8'] + T['8max'][1] * (1 - slider['8'])]           
           

    def arm_draw(colour = GREY,thickness = 3):
        
        # Pedestal
        pygame.draw.line(screen, colour, T['01'], T['02'], thickness)
        pygame.draw.line(screen, colour, T['02'], T['03'], thickness)
        pygame.draw.line(screen, colour, T['03'], T['04'], thickness)
        pygame.draw.line(screen, colour, T['04'], T['01'], thickness)
        pygame.draw.line(screen, colour, T['1'], [T['1'][0],T['1'][1]+f05], thickness)

        # Shoulder
        pygame.draw.line(screen, colour, T['1'],  T['15'], thickness)
        pygame.draw.line(screen, colour, T['15'], T['2'],  thickness)
        pygame.draw.line(screen, colour, T['1'],  T['2'],  thickness)

        # Elbow, wrist
        pygame.draw.line(screen, colour, T['2'],  T['3'],  thickness)
        pygame.draw.line(screen, colour, T['3'],  T['4'],  thickness)

        # Claw
        pygame.draw.line(screen, colour, T['51'], T['52'], thickness)
        pygame.draw.line(screen, colour, T['52'], T['53'], thickness)
        pygame.draw.line(screen, colour, T['53'], T['54'], thickness)
        pygame.draw.line(screen, colour, T['54'], T['51'], thickness)
        pygame.draw.line(screen, colour, T['51'], T['53'], thickness-1)
        pygame.draw.line(screen, colour, T['52'], T['54'], thickness-1)
    
    def rotators_draw(colour = WHITE, thickness = 1):
        for n in slider:
            pygame.draw.line(screen, colour, T[n+'min'], T[n+'max'], thickness)
            
    def joint(x, rad, colour):
        
        if x == None:
            return 0
        
        #Coloured circle
        pygame.draw.circle(screen, colour, [T[x][0]+1,T[x][1]+1], rad)

        if textable(x):
            text('T'+x,list(map(add,T[x],jointSHIFT)))

        #Black center
        if hover == x:
            pygame.draw.circle(screen, BLACK, [T[x][0]+1,T[x][1]+1], rad-2)
            
        else:
            pygame.draw.circle(screen, BLACK, [T[x][0]+1,T[x][1]+1], rad-1)

    def drawable(p):
        return (textable(p) or clickable(p) or dragable(p))

    def movable(p):
        return (
                p == '2' or 
                p == '3' or
                p == '4'
                )

    def textable(p):
        return (p == '1' or p == '0' or movable(p))

    def clickable(p):
        return (p == 'amode' or
                p == 'smode' or
                p == 'speed' or
                p == 'exit' or
                p == 'limits' or
                p == 'live' or
                p == 'rainbow'
                )

    def dragable(p):
        return (p == '0s' or
                p == '7' or
                p == '8')

    def joints_draw():
        for p in T:
            
            if drawable(p):
                joint(p, psize[p], pcolour[p])
                    
            #else:
                #joint(p, 2, YELLOW)

    def cplxp(point):
        return complex(point[0],point[1])

    def get_mangle(): # For click time

        #Perhaps def func for this
        p = '1'
        fa1 = 0
        fa2 = 0
        if hover == '3':
            p = '2'
            fa1 = 1
        elif hover == '4':
            p = '3'
            fa1 = 1
            fa2 = 1
            
        c1 = cplxp(T[p])
        c2 = cplxp(T['m'])
        
        return  cmath.phase((c1 - c2) * (cos(-pi2 - fa1 * Tangle['1'] - fa2 * Tangle['2']) +
                        complex(0, 1) *  sin(-pi2 - fa1 * Tangle['1'] - fa2 * Tangle['2'])))

    def get_angles():

        c1 = cplxp(T['1'])
        c2 = cplxp(T['2'])
        
        T1 = cmath.phase((c1 - c2) * (cos(-pi2) +
                     complex(0, 1) *  sin(-pi2)))
        
        c1 = cplxp(T['2'])
        c2 = cplxp(T['3'])
        
        T2 = cmath.phase((c1 - c2) * (cos(-T1 - pi2) +
                     complex(0, 1) *  sin(-T1 - pi2)))
        
        c1 = cplxp(T['3'])
        c2 = cplxp(T['4'])
        
        return T1, T2, cmath.phase((c1 - c2) * (cos(-T2 - T1 - pi2) +
                               complex(0, 1) *  sin(-T2 - T1 - pi2)))

    def angles_write():
        Tangle['1'], Tangle['2'], Tangle['3'] = get_angles()
        if MODES['amode'] == 'deg':
            for n in Tangle:
                text(Tangle[n]*180/pi, T[n])
        elif MODES['amode'] == 'rad':
            for n in Tangle:
                text(Tangle[n], T[n])
        elif MODES['amode'] == 'pos':
            for n in Tangle:
                text(int((Tangle[n]-linear_b[n])/linear_k[n]), T[n])
    
    def sliders_write():
        if MODES['smode'] == 'sld':
            for n in slider:
                if T[n+'max'][0] != T[n+'min'][0]: #H
                    text(slider[n], list(map(add,[(T[n+'max'][0]+T[n+'min'][0])/2,T[n][1]], sliderSHIFT)))
                else:
                    text(slider[n], list(map(add,[T[n][0],(T[n+'max'][1]+T[n+'min'][1])/2], modesSHIFT)))
        elif MODES['smode'] == 'rad':
            for n in slider:
                if T[n+'max'][0] != T[n+'min'][0]: #H
                    text((slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n])*linear_k[n]+linear_b[n], list(map(add,[(T[n+'max'][0]+T[n+'min'][0])/2,T[n][1]], sliderSHIFT)))
                else:
                    text((slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n])*linear_k[n]+linear_b[n], list(map(add,[T[n][0],(T[n+'max'][1]+T[n+'min'][1])/2], modesSHIFT)))
        elif MODES['smode'] == 'deg':
            for n in slider:
                if T[n+'max'][0] != T[n+'min'][0]: #H
                    text(((slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n])
                         *linear_k[n]+linear_b[n])*180/pi,
                         list(map(add,[(T[n+'max'][0]+T[n+'min'][0])/2,T[n][1]], sliderSHIFT)))
                else:
                    text(((slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n])*linear_k[n]+linear_b[n])*180/pi, list(map(add,[T[n][0],(T[n+'max'][1]+T[n+'min'][1])/2], modesSHIFT)))

        else:
            for n in slider:
                if T[n+'max'][0] != T[n+'min'][0]: #H
                    text(int(slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n]), list(map(add,[(T[n+'max'][0]+T[n+'min'][0])/2,T[n][1]], sliderSHIFT)))
                else:
                    text(int(slider[n]*(MAX_POS[n]-MIN_POS[n])+MIN_POS[n]), list(map(add,[T[n][0],(T[n+'max'][1]+T[n+'min'][1])/2], modesSHIFT)))
         
    def buttons_write():
        shift = [36,0]
        for m in MODES:
            text('- '+m, list(map(add,T[m],list(map(add,modesSHIFT,shift))))) 
                         
    def get_hover():
        for p in T:
            if p == 'm':
                continue
            if abs(T['m'][0] - T[p][0]) < JRAD:
                if abs(T['m'][1] - T[p][1]) < JRAD:
                    return p

    def rainbow():
        red = (sin(rainbowcount)+1)*255/2
        green = (sin(rainbowcount+2*pi/3)+1)*255/2
        blue = (sin(rainbowcount+4*pi/3)+1)*255/2
        return (red,green,blue)

    def change_mode(m):
        if m == 'amode':
            if MODES[m] == 'rad':
                MODES[m] = 'deg'
            elif MODES[m] == 'deg':
                MODES[m] = 'pos'
            else:
                MODES[m] = 'rad'
        elif m == 'speed':
            if MODES[m] == 1:
                MODES[m] = 10
            elif MODES[m] == 10:
                MODES[m] = 100
            else:
                MODES[m] = 1
        elif m == 'smode':
            if MODES[m] == 'sld':
                MODES[m] = 'rad'
            elif MODES[m] == 'rad':
                MODES[m] = 'deg'
            elif MODES[m] == 'deg':
                MODES[m] = 'pos'
            else:
                MODES[m] = 'sld'
        else:
            if MODES[m]:
                MODES[m] = False
            else:
                MODES[m] = True
                
    def modes_write():
        for m in MODES:
            text(MODES[m], list(map(add,T[m],modesSHIFT)))

    #Main
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    font = pygame.font.SysFont(FONT, FONT_SIZE)


    get_pos()       
    calculate_arm()

    #Main    
    while MODES['exit']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MODES['exit'] = False
            elif event.type == pygame.MOUSEBUTTONUP:
                MPRESS = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MPRESS = True
                
        screen.fill(BLACK)
        rainbowcount = (rainbowcount + 0.1) % 6.28318530718
        T['m'] = pygame.mouse.get_pos()
        
        axes_draw()
        if MODES['rainbow']:
            arm_draw(rainbow())
            rotators_draw(rainbow())
        else:
            arm_draw()
            rotators_draw()
        pcolour['rainbow'] = rainbow()
        joints_draw()
        modes_write()
        angles_write()
        sliders_write()
        buttons_write()
        
        if not MPRESS:
            hover = get_hover()
            
        if MPRESS:
            if movable(hover):
                            
                p = '1'
                if hover == '3':
                    p = '2'
                elif hover == '4':
                    p = '3'
                    
                dAngle = get_mangle() - Tangle[p]

                if MODES['limits']:
                    Tangle[p] = min(linear_k[p]*MAX_POS[p]+linear_b[p],
                                max(linear_k[p]*MIN_POS[p]+linear_b[p],
                                    Tangle[p] + dAngle/MODES['speed']))
                else:
                    Tangle[p] = Tangle[p] + dAngle/MODES['speed']

                if MODES['live'] and port != None:
                    servo1 = 0
                    servo2 = 0
                    if p == '1':
                        servo1 = 2
                        servo2 = 3
                    elif p == '2':
                        servo1 = 5
                        servo2 = 4
                    else:
                        servo1 = 6
                    pos = int((Tangle[p]-linear_b[p])/linear_k[p])
                    pos1 = 1023 - pos
                    if servo2 != 0:
                        port.setReg(servo1, P_GOAL_POSITION_L, [pos%256,pos>>8])
                        port.setReg(servo2, P_GOAL_POSITION_L, [pos1%256,pos1>>8])
                    else:
                        port.setReg(servo1, P_GOAL_POSITION_L, [pos%256,pos>>8])
                        
                        
                calculate_arm()
                
            elif clickable(hover):

                change_mode(hover)
                MPRESS = False

            elif dragable(hover):

                mi = hover + 'min'
                ma = hover + 'max'
                
                dSlider = T['m'][0]
                
                if T[mi][0] == T[ma][0]: #vertical
                    dSlider = float(T['m'][1] - T[hover][1])
                else:
                    dSlider = float(T['m'][0] - T[hover][0])
                    
                T[hover] = [min(max(T[mi][0],T[hover][0]+dSlider/MODES['speed']),T[ma][0]),
                            min(max(T[mi][1],T[hover][1]+dSlider/MODES['speed']),T[ma][1])]
                
                if T[ma][0] == T[mi][0]:
                    slider[hover] = (T[hover][1] - T[ma][1]) / (T[mi][1] - T[ma][1])
                elif T[ma][1] == T[mi][1]:
                    slider[hover] = (T[hover][0] - T[mi][0]) / float(T[ma][0] - T[mi][0])
                    
                if MODES['live'] and port != None:
                    pos = int(slider[hover]*(MAX_POS[hover]-MIN_POS[hover])+MIN_POS[hover])
                    ctext(pos)
                    if hover == '0s':
                        port.setReg(1, P_GOAL_POSITION_L, [pos%256,pos>>8])
                    elif hover == '7':
                        port.setReg(7, P_GOAL_POSITION_L, [pos%256,pos>>8])
                    elif hover == '8':
                        port.setReg(8, P_GOAL_POSITION_L, [pos%256,pos>>8])

        #Essentials
        pygame.display.flip()
        clock.tick(60)
        
    return pygame.quit()













