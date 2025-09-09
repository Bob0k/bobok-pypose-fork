import numpy as np
import random
from math import tanh

def rand(i):
    return random.uniform(-1,1)

class Network:

    def __init__(self, weights = 0):
        if type(weights) == int:
            self.weights = np.stack([np.identity(3)])
        else:
            self.weights = weights
        self.actfunc = tanh

##    def randomize(self):
##        self.weights = np.vectorize(rand)(self.weights)
        
    def run(self, input_):
        level = input_
        for w in self.weights:
            for i in range(len(level)):
                level[i] = self.actfunc(level[i])
            #level = np.vectorize(actfunc)(level)
            level = np.tensordot(level, w, axes = 1)
        return level
    
    def has_identity_layers(self):
        pass

    def mutate(self, regime = None):
        if regime == None:
            regime = random.randrange(2)
        if regime == 0: # Randomize random link
            w = random.randrange(len(self.weights))
            i = random.randrange(len(self.weights[w]))
            j = random.randrange(len(self.weights[w][i]))
            self.weights[w][i][j] = rand(0)
        elif regime == 1: # Add hidden identity layer
            self.weights = np.concatenate((self.weights,
                                           [np.identity(3)]),
                                          axis = 0)

    def show(self, w = None):
        if w == None:
            for w in self.weights:
                print(w)
        else:
            print(self.weights[w])

if __name__ == '__main__':
    net = Network()

    from datetime import datetime
    amount = 200000
    if not (int(net.run([1,2,3])[0] * 100000000) ==  76159415
           and int(net.run([1,2,3])[1] * 100000000) == 96402758
           and int(net.run([1,2,3])[2] * 100000000) == 99505475):
        print('Result is wrong')
    start = datetime.now()
    for i in range(amount):
        net.run([1,2,3])
    time = datetime.now() - start
    print('Total time:', time)
    time = time.seconds * 1000000.0 + time.microseconds 
    print('For each run:', time / amount)
