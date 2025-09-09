
"""Neural network class v1

This version uses simple list for storing nodes
"""

import random
import copy
from math import e

_MAX_WEIGHT = 10

def proportional_pick(chances):
    
    anynegatives = False
    for c in chances:
        if c < 0:
            anynegatives = True
            break
    if anynegatives:
        min_ = min(chances)
        chances = [c - min_ for c in chances]
    sum_ = sum(chances)
    if sum_ == 0:
        return random.randrange(0,len(chances))
    chances = [c/float(sum_)*100 for c in chances]
    mutatemode = random.randint(1,int(sum(chances)))
    choice = 0
    for i in range(len(chances)):
        choice += chances[i]
        if choice >= mutatemode:
            return i
        
##def ppick_test(ch):
##    res = [0 for i in ch]
##    for i in range(1000):
##        res[proportional_pick(ch)] += 1
##    sum_ = sum(res)
##    for i in range(len(res)):
##        res[i] = res[i] / float(sum_) * 100
##    for i in range(len(res)):
##        print i,'-',str(res[i])+'%'
##
##ppick_test([
##        -1,
##        -2,
##        -3,
##        -4,
##        -5
##        -20,
##        -30,
##        -40,
##        -50
##        ])
    
def _sigmoid(x):
    return 1/(1+e**(-x))

def _tangensoid(x):
    return 2/(1+e**(-x))-1
    
class Node:

    def __init__(self, links = []):
        self.links = copy.copy(links)
        self.signal = 0
        self.bias_weight = 0
    def add_link(self, lvlto, nto, weight):
        for i in range(len(self.links)):
            if self.links[i][0] == lvlto and self.links[i][1] == nto:
                self.links[i] = [lvlto, nto, weight]
                print 'Error: add_link used to modify'
                return 1
        self.links.append([lvlto, nto, weight])
        return 0

    def del_link(self,lvlto,nto):
        for i in range(len(self.links)):
            if self.links[i][0] == lvlto and self.links[i][1] == nto:
                self.links.pop(i)
                return 0
        print('Error: Tried to delete not existing link')
        return 1/0
        
    def show(self,title = ''):
        print(title)
        print('Links:')
        print(self.links)
        print('Signal:')
        print(self.signal)
        print('Bias:')
        print(self.bias_weight)

        
class Network:
    
    def __init__(self,
                 ins,      # Number of input neurons
                 outs,     # Number of output neurons
                 maxlevel, # Number of hidden layers
                 mnpl,     # Max number of neurons per level
                 biased = True,
                 #init_weight = 0,
                 sigmoid = True
                 ):
        if sigmoid:
            self._actfunc = _sigmoid
        else:
            self._actfunc = _tangensoid
        self.mnpl = mnpl
        self.biased = biased
        self.node = [[] for i in range(maxlevel+2)]
        for i in range(outs):
            self.node[maxlevel+1].append(Node())
        for i in range(ins):
            self.node[0].append(Node())

    def control_sum(self):
        csum = 0
        csum += self.mnpl
        for lvl in range(len(self.node)):
            for n in range(len(self.node[lvl])):
                csum += lvl + n
                for link in self.node[lvl][n].links:
                    csum += int(sum(link))
        if self._actfunc.__name__ == '_sigmoid':
            csum *= -1
        return csum
    
    def get_not_empty_levels(self):
        levels = list()
        for lvl in range(1,len(self.node)):
            if self.node[lvl]:
                levels.append(lvl)
        return levels
    
    def get_avail_levels(self):
        levels = list()
        for lvl in range(1,len(self.node)-1):
            if len(self.node[lvl]) < self.mnpl:
                levels.append(lvl)
        return levels

    def max_links(self, level):
        maxlinks = 0
        for lvl in range(level+1,len(self.node)):
            maxlinks += len(self.node[lvl])
        return maxlinks
                
    def get_not_full_nodes(self):
        nodes = list()
        for lvl in range(len(self.node)):
            maxl = self.max_links(lvl)
            for n in range(len(self.node[lvl])):
                if len(self.node[lvl][n].links) < maxl:
                    nodes.append((lvl,n))
        return nodes
        
    def get_hidden_nodes(self):
        nodes = list()
        for lvl in range(1,len(self.node)-1):
            for n in range(len(self.node[lvl])):
                nodes.append((lvl,n))
        return nodes

    def get_avail_nodes(self, level, num):
        nodes = list()
        for lvl in range(level+1,len(self.node)):
            for n in range(len(self.node[lvl])):
                found_node_in_links = False
                for link in self.node[level][num].links:
                    if lvl == link[0] and n == link[1]:
                        found_node_in_links = True
                        break
                if not found_node_in_links:
                    nodes.append((lvl,n))
        return nodes
                    
    def get_links(self):
        linkslist = list()
        for lvl in range(len(self.node)):
            for n in range(len(self.node[lvl])):
                for i in range(len(self.node[lvl][n].links)):
                    linkslist.append([lvl,n,i])
        return linkslist
        
    def add_node(self, level):
        if level == 0:
            print('Error: Adding input node')
            return 1
        elif level == len(self.node) - 1:
            print('Error: Adding output node')
            return 1
        elif len(self.node[level]) >= self.mnpl:
            print('Error: Layer overfilled')
            return 1
        self.node[level].append(Node())
    
    def show(self, title=''):
        print title
        for lvl in range(len(self.node)):
            for n in range(len(self.node[lvl])):
                if lvl == 0:
                    self.node[lvl][n].show('\nInput node #'+str(n+1))
                elif lvl == len(self.node) - 1:
                    self.node[lvl][n].show('\nOutput node #'+str(n+1))
                else:
                    self.node[lvl][n].show('\nLevel '
                                           +str(lvl)
                                           +' node #'+str(n+1))
            
    def run(self, inp):
        for lvl in self.node:
            for n in lvl:
                n.signal = 0
        for n in range(len(self.node[0])):
            self.node[0][n].signal = inp[n]
        for lvl in self.node:
            for n in lvl:
                if self.biased:
                    n.signal += n.bias_weight
                for link in n.links:
                    self.node[link[0]][link[1]].signal += \
                        self._actfunc(n.signal) * link[2]
        return [n.signal for n in self.node[len(self.node)-1]]

    def mutate(self, mode = None):
        if mode == None:
            mode = proportional_pick(
                [33, # New node
                 200, # New link
                 100, # Modify link
                 100, # Modify bias
                 1,  # Delete link
                 0,  # Delete neuron
                 ])
        if mode == 0:   # New node
            mode = self.get_avail_levels()
            if mode:
                self.add_node(random.choice(mode))
                return 0
            #print 'Error: No room for a new node'
            return self.mutate(proportional_pick(
                [0, # New node
                 66, # New link
                 100, # Modify link
                 100, # Modify bias
                 1,  # Delete link
                 0,  # Delete neuron
                 ])
                               )
        elif mode == 1: # New link
            mode = self.get_not_full_nodes()
            if mode:
                mode = random.choice(
                    mode
                    )
                tonode = random.choice(
                    self.get_avail_nodes(mode[0],mode[1])
                    )
                self.node[mode[0]][mode[1]].add_link(
                    tonode[0],
                    tonode[1],
                    random.npercent()
                    )
                return 1
            #print 'Error: No not full nodes'
            return self.mutate(proportional_pick(
                [50, # New node
                 0, # New link
                 100, # Modify link
                 10, # Modify bias
                 50,  # Delete link
                 0,  # Delete neuron
                 ])
                               )
        elif mode == 2: # Modify link
            mode = self.get_links()
            if mode:
                mode = random.choice(mode)
                self.node[mode[0]
                        ][mode[1]].links[
                                        mode[2]][2] = random.npercent()*_MAX_WEIGHT
                return 2
            #print 'Error: There is no links to modify'
            return self.mutate(proportional_pick(
                [33, # New node
                 500, # New link
                 0, # Modify link
                 100, # Modify bias
                 0,  # Delete link
                 0,  # Delete neuron
                 ])
                               )
        elif mode == 3: # Modify bias
            mode = self.get_not_empty_levels()
            if mode:
                mode = random.choice(mode)
                self.node[mode][random.randint(0,
                               len(self.node[mode])-1)
                                ].bias_weight = random.npercent()
                return 3
            print 'Error: Trying to modify bias of non-existant node'
            return -1
        
        elif mode == 4: # Delete link
            mode = self.get_links()
            if mode:
                mode = random.choice(mode)
                self.node[mode[0]][mode[1]].links.pop(mode[2])
                return 4
            #print 'Error: There is no links to delete'
            return self.mutate(proportional_pick(
                [33, # New node
                 500, # New link
                 0, # Modify link
                 10, # Modify bias
                 0,  # Delete link
                 0,  # Delete neuron
                 ])
                               )
        elif mode == 5: # Delete node
            mode = self.get_hidden_nodes()
            if mode:
                mode = random.choice(mode)
                self.node[mode[0]].pop(mode[1])
                for lvl in range(0,mode[0]):
                    for n in range(len(self.node[lvl])):
                        for i in range(len(self.node[lvl][n].links)):
                            if (self.node[lvl][n].links[i][0] == mode[0]
                                    and self.node[lvl][n].links[i][1] == mode[1]):
                                self.node[lvl][n].links.pop(i)
                                break
                return 5
            print 'Error: No hidden nodes'
            
            return self.mutate(0)
        else:
            print 'Error: Wrong mutate regime'
            return -1
        
