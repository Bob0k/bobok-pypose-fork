#Perceptrone

import random
from copy import deepcopy
#from AIconstants import *
from constants import *

def actfunc(input):
  return 1/(1+e**-input)
  #return 2/(1+e**-input)-1

e = 2.71828182845904523536

OUTPUT_NEURONS = 2
INPUT_NEURONS = 2

W_INITIAL = 0
MAX_LEVEL = 2
MAX_NODES_PER_LEVEL = 2
MAX_NODES = (MAX_LEVEL - 1) * MAX_NODES_PER_LEVEL + OUTPUT_NEURONS + INPUT_NEURONS

W_INITIAL = 0.5
W_ACC = 1000 # 10 ^ Max amount of numbers after dot in float weigth value


# 1. Generation is born
# 2. Generation is evaluated
# 3. Generation has given a new one:
#top ten percent is kept without modification
#Chance of picking specie is proportional to its score
#Mutations can be:
#A new connection
#A new node
#A modification of existing connection
#Repeat until population is full
# 3.1. Save best result
# 4. Goto 2.
#
# Errors found:
# 1. Vertical connections                        [?]
# 2. Weights can be only -1, -0.5(?), 0, 0.5, 1  [?]
# 3. Mutations tend to slow down                 [-]
#    - to solve that one it is needed to change
#    - nodes chosing algorithm  under  Mutate()
# 4. Nodes can't reach maximum                   [+]
# 5. 

class Neuron:
  def __init__(self, level, nid, neurarr = list()):

    self.nid = nid
    self.signal = 0
    self.level = 0

    if level <= MAX_LEVEL:
      self.level = level

    self.links = self.linksinit(neurarr)

  def linksinit(self, neurarr):
    temp = list()
    if self.level == 0:
      if len(neurarr) > 0:
        for i in neurarr:
          if i.level > self.level:
                        #i,   wi
            temp.append([i.nid,W_INITIAL])

    return temp

class Network:

  def __init__(self):

    self.node = list()
    self.nid = 0

    #Output neurons:
    for i in range(OUTPUT_NEURONS):
      self.node.append(Neuron(MAX_LEVEL,self.nid))
      self.nid += 1

    #Input neurons:
    for i in range(INPUT_NEURONS):
      self.node.append(Neuron(0,self.nid,self.node))
      self.nid += 1

  def AddNode(self,lvl,connectto = None,connectw = W_INITIAL):

    self.node.append(Neuron(lvl,self.nid,self.node))
    self.nid += 1

    if type(connectto) == int and connectto < self.nid:

      flag2 = False

      for link in self.node.links: #Check link on existance
        if link[0] == connectto: #if this link is existing
          flag2 = True
          break

      self.node.links.append([connectto, connectw])


  def CountPossibleLinks(self,i):
    temp = 0
    ids = list()
    for n in self.node:
      if n.level > self.node[i].level:
        temp += 1
        ids.append(n.nid)
    return temp, ids

  def Show(self, title = ''):
    print(title)
    for n in self.node:
      print('i =', n.nid)
      if n.level != 0 and n.level != MAX_LEVEL:
        print('Level =', n.level, '\nLinks:')
      elif n.level == 0:
        print('Level = Input\nLinks:')
      else:
        print('Level = Output\nLinks:')
      print(n.links)
      print('signal =', n.signal)
      print('\n')

  def Run(self,inputs): #Give inputs - get answers. Easy enough

    #Flushing signals
    for i in range(OUTPUT_NEURONS):
      self.node[i].signal = 0
    for i in range(OUTPUT_NEURONS,OUTPUT_NEURONS+INPUT_NEURONS):
      self.node[i].signal = inputs[i-OUTPUT_NEURONS]
    for i in range(OUTPUT_NEURONS+INPUT_NEURONS,len(self.node)):
      self.node[i].signal = 0

    #Signal transfer
    for lv in range(MAX_LEVEL):
      for i in range(OUTPUT_NEURONS,len(self.node)):
        if self.node[i].level != lv:
          continue
        for l in self.node[i].links:
          #if lv == -1:
            #self.node[l[0]].signal += self.node[i].signal * l[1]
          #else:
          self.node[l[0]].signal += actfunc(self.node[i].signal) * l[1]
          #self.node[l[0]].signal += actfunc(self.node[i].signal) * l[1]

    outs = list()
    for i in range(OUTPUT_NEURONS):
      outs.append(actfunc(self.node[i].signal))

    return outs

  def LvlQ(self,lvl): #Quantity of nodes on level?
    count = 0
    for n in self.node:
      if n.level == lvl:
        count += 1
    return count

  def Mutate(self):
    # 0 - New connection
    # 1 - New node
    # 2 - Modification of existing connection
    i = random.randint(0,2) #Choose mutation rout

    while 1:

      if i == 0:

        #Check if there is any missing connections
        possiblelinks = 0
        for j in range(len(self.node)):
          possiblelinks += self.CountPossibleLinks(j)[0]
        for n in self.node:
          possiblelinks -= len(n.links)

        AllConnections = False
        if possiblelinks == 0:
          AllConnections = True

        while not AllConnections:
          i = random.randint(1,len(self.node)-1) #Choose node to make link from
          numposslinks, ids = self.CountPossibleLinks(i)
          #print 'numposslinks -', numposslinks
          #print 'ids -', ids
          #print 'i -', i
          #print 'len(self.node[i].links) -', len(self.node[i].links)
          
          if numposslinks > len(self.node[i].links): #If there is missing connection on chosen node

            flag2 = True
            while flag2:
              
              j = random.choice(ids) #Choose node to make link to
              #print 'j -', j             
              flag2 = False
              
              for link in self.node[i].links: #Check link on existance 
                if link[0] == j: #if this link is existing               
                  flag2 = True
                  break

              if not flag2:
                self.node[i].links.append([j,W_INITIAL])
                return 0

          else:
            break
        else: #If AllConnections
          
          i = random.randint(1,2)

      elif i == 1:
        if len(self.node) < MAX_NODES:
          i = random.randint(1,MAX_LEVEL-1)
          while self.LvlQ(i) == MAX_NODES_PER_LEVEL: # Choses a level to create a node
            i = random.randint(1,MAX_LEVEL-1)
          self.AddNode(i)

          # Creating links to the new node
          i = random.randint(1,len(self.node)-2) #Choose node to make link from
          while self.node[i].level > self.node[-1].level:
            i = random.randint(1,len(self.node)-1) #Choose node to make link from

          self.node[i].links.append([self.node[-1].nid,W_INITIAL])

          # Choose node to make link to
          ids = self.CountPossibleLinks(-1)[1]
          i = random.randint(0,len(ids)-1)
          self.node[-1].links.append([ids[i],W_INITIAL])

          return 1
        else:
          
          i = random.randint(0,1)*2

      else:
        i = random.randint(1,len(self.node)-1) #Choose a node
        if len(self.node[i].links) == 0:
          i = random.randint(0,1)
          continue
        j = random.randint(0,len(self.node[i].links)-1) #Choose a link
        self.node[i].links[j][1] = random.randint(-W_ACC,W_ACC)/float(W_ACC) #Set random weigth
        return 2
    return -1

class Generation:

  def __init__(self):
    self.nets = list()
    self.arms = list()
    global W_INITIAL
    W_INITIAL = -1
    for i in range(MAX_SPECIES):
      self.nets.append(Network())
##      tempcolour = ((255/MAX_SPECIES*i)%255,
##                    (255/MAX_SPECIES*(i+1))%255,
##                    (255/MAX_SPECIES*(i+2))%255)
      #tempcolour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
      #self.nets[i].colour = tempcolour
      self.arms.append(Arm(tempcolour))
      W_INITIAL = 2.0/MAX_SPECIES*i-1

    self.scores = [0 for i in range(MAX_SPECIES)]

  def __len__(self):
    return len(self.nets)

  def Draw(self,screen):
    for i in range(MAX_SPECIES):
        self.arms[i].draw(screen,self.nets[i].colour)
        
  def Show(self):
    for i in self.nets:
      i.Show()
      
  def Sort(self, Descending = True):

    sortlist = SortedList(self.scores, Descending)

    sortednetworks = list()
    sortedscores = list()
    for i in range(len(sortlist)):
      sortednetworks.append(deepcopy(
          self.nets[sortlist[i][0]]
                                     ))
      sortedscores.append(deepcopy(
          self.scores[sortlist[i][0]]
                                     ))

    self.nets = sortednetworks
    self.scores = sortedscores

  def GetScores(self, input = [[0],[1],[2]]):

    for i in range(len(self.nets)):
      self.scores[i] = 0

    for i in range(len(self.nets)):
      for inpu in input:
        self.scores[i] += self.nets[i].Run(inpu)[0]


  def NextGeneration(self): #Get new generation

    #Generation sort
    self.Sort()
    #Sorted Evaluation

    if AnyNegatives(self.scores):
      m = 2*min(self.scores)
      for i in range(len(self.scores)):
        self.scores[i] -= m

    ss = sum(self.scores)
    self.scores[0] /= ss
    for i in range(1,len(self.scores)):
      self.scores[i] = self.scores[i]/ss + self.scores[i-1]

    newnets = list()

    for i in range(len(self.scores)):
      if self.scores[i] < MUTATION_THRESHOLD:
        newnets.append(deepcopy(self.nets[i]))
      else:
        break

    while len(newnets) < MAX_SPECIES:
      r = random.percent()

      i = 0
      while r > self.scores[i]:
        i += 1
      i -= 1

      mutnet = deepcopy(self.nets[i])
      mutnet.Mutate()
      
      newnets.append(mutnet)

    else:
      self.nets = newnets
      for n in self.nets:
        n.mark = False
      
    for s in self.scores:
      s = 0
    
  def Save(self, name = 'SavedNets'):
    import datetime
    filename = 'saves/'+name+str(datetime.datetime.now()).replace(':','')+'.txt'
    with open(filename,'w') as f:
      for sp in self.nets:
        for i in range(len(sp.node)):
          f.write(str(i)+'\t'+str(sp.node[i].links)+'\t'
                  +str(sp.node[i].level)+'\n')
          
  def Load(self,filename):
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
            self.nets[i].AddNode(int(line[line.rfind('\t')+1:-1]))
            
        self.nets[i].node[int(line[:line.find('\t')])].links = temp



#Generation born
##gen = Generation()
##
##for i in range(len(gen)):
##  gen[i].Mutate()
##  gen[i].Mutate()
##
##for g in range(MAX_GEN):
##
##  #Evaluation
##  gen.GetScores()
##
##  gen.NextGeneration()
##
##gen.Sort()
##print(gen.GetScores())
