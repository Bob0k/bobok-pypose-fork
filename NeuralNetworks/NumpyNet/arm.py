"""Arm class"""

from math import sin, cos

_pi2 = 1.57079632679
_T1 = [380, 460]

#Arm dimensions
_TRIANGLE_LENGTH = 144.7
#_TRIANGLE_HEIGHT = 36.4
_TRIANGLE_HYP = 149.25
_TRIANGLE_ANGLE = 0.246441600965

_FOREARM_LENGTH = 145.7

_HAND_LENGTH = 114.75

_CLAW_LENGTH = 36
_CLAW_HEIGHT = 28.1

_MIN_POS = {
    '1': -1.32435471248,
    '2': -0.523598771149,
    '3': -1.76714585263,
}
_MAX_POS = {
    '1': 1.81723791441,
    '2': 2.87979324132,
    '3': 1.96349539181,
}

_ROTATE_SPEED = 1#00
    
class Arm():
    
    def __init__(self):
        self.T = {}
        self.Tangle = {}
        self.set_default_pos()

    def set_default_pos(self):
        self.Tangle = {
            '1':  0.2815712309782569,
            '2':  1.3360390799742112,
            '3':  0.829875124161613
            }
        self.calculate_2()
        
    def calculate_2(self):
        self.T['2'] = [
            _T1[0] + _TRIANGLE_HYP * cos(self.Tangle['1'] - _pi2),
            _T1[1] + _TRIANGLE_HYP * sin(self.Tangle['1'] - _pi2)
            ]
        self.T['15'] = [
            _T1[0] + _TRIANGLE_LENGTH * cos(self.Tangle['1'] - _TRIANGLE_ANGLE - _pi2),
            _T1[1] + _TRIANGLE_LENGTH * sin(self.Tangle['1'] - _TRIANGLE_ANGLE - _pi2)
            ]
        self.calculate_3()
        
    def calculate_3(self):
        self.T['3'] = [
            self.T['2'][0] + _FOREARM_LENGTH * cos(self.Tangle['1']
                                      + self.Tangle['2']
                                      - _pi2),
            self.T['2'][1] + _FOREARM_LENGTH * sin(self.Tangle['1']
                                      + self.Tangle['2']
                                      - _pi2)
            ]
        self.calculate_4()
        
    def calculate_4(self):
        cosx = cos(self.Tangle['1']
                   + self.Tangle['2']
                   + self.Tangle['3'])
        sinx = sin(self.Tangle['1']
                   + self.Tangle['2']
                   + self.Tangle['3'])
        self.T['4'] = [
            self.T['3'][0] + _HAND_LENGTH * sinx,
            self.T['3'][1] - _HAND_LENGTH * cosx]
        self.T['5'] = [
            self.T['3'][0] + (_HAND_LENGTH+_CLAW_LENGTH/2) * sinx,
            self.T['3'][1] - (_HAND_LENGTH+_CLAW_LENGTH/2) * cosx]
        self.T['51'] = [
            self.T['4'][0] - _CLAW_HEIGHT/2 * cosx,
            self.T['4'][1] - _CLAW_HEIGHT/2 * sinx]
        self.T['52'] = [
            self.T['51'][0] + _CLAW_LENGTH * sinx,
            self.T['51'][1] - _CLAW_LENGTH * cosx]
        self.T['53'] = [
            self.T['52'][0] + _CLAW_HEIGHT * cosx,
            self.T['52'][1] + _CLAW_HEIGHT * sinx]
        self.T['54'] = [
            self.T['53'][0] - _CLAW_LENGTH * sinx,
            self.T['53'][1] + _CLAW_LENGTH * cosx]
                    
    def move_to(self, p, destination):
        dAngle = destination - self.Tangle[p]
        
        self.Tangle[p] = (min(_MAX_POS[p],
                    max(_MIN_POS[p],
                        self.Tangle[p] + dAngle/_ROTATE_SPEED))) 
        if p == '1':
            self.calculate_2()
        elif p == '2':
            self.calculate_3()
        elif p == '3':
            self.calculate_4()
            
    def move_all(self, d1, d2 = None, d3 = None):
        if d2 == None:
            self.move_to('1', d1[0])
            self.move_to('2', d1[1])
            self.move_to('3', d1[2])
        else:
            self.move_to('1', d1)
            self.move_to('2', d2)
            self.move_to('3', d3)

    def get_angles(self):
        return [self.Tangle['1'],
                self.Tangle['2'],
                self.Tangle['3']]
    
    def get_points(self):
        return [self.T['2'],
                    _T1,
                self.T['15'],
                self.T['2'],
                self.T['3'],
                self.T['4'],
                self.T['51'],
                self.T['52'],
                self.T['53'],
                self.T['54'],
                self.T['52']],[self.T['53'],
                               self.T['51'],
                               self.T['54']]
