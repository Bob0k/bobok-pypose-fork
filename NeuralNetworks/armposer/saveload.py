"""Neural network saver loader v1"""
from neuralnetwork import *
    
def random_savename():
    savename = ''
    with open('names/nouns.txt','r') as f:
        nouns = [line[:-1] for line in f]
    with open('names/adjectives.txt','r') as f:
        adjectives = [line[:-1] for line in f]
        
    import random
    return random.choice(adjectives)+' '+random.choice(nouns)

def loadnet(savename):
    scorings = list()
    with open('saves/'+savename+'/scorings.txt','r') as f:
        for line in f:
            if line != '\n':
                scorings.append(line[:-1])
    inputs = list()
    with open('saves/'+savename+'/inputs.txt','r') as f:
        for line in f:
            if line != '\n':
                inputs.append(line[:-1])
    gencount = 0
    maxtime = 0
    with open('saves/'+savename+'/generation.txt','r') as f:
        fl = True
        for line in f:
            if line != '\n':
                if fl:
                    gencount = int(line[:-1])
                    fl = False
                else:
                    maxtime = int(line[:-1])
    nets = list()
    gen = None
    with open('saves/'+savename+'/net.txt','r') as f:
        oldlvl = 0
        nets.append([])
        ins = None
        outs = None
        maxlevel = None
        mnpl = None
        biased = None
        i = -6
        for line in f:
            if i == -6:
                ins = int(line[:line.find(' ')])
                i += 1
                continue
            elif i == -5:
                outs = int(line[:line.find(' ')])
                i += 1
                continue
            elif i == -4:
                maxlevel = int(line[:line.find(' ')])
                i += 1
                continue
            elif i == -3:
                mnpl = int(line[:line.find(' ')])
                i += 1
                continue
            elif i == -2:
                biased = bool(line[:line.find(' ')])
                i += 1
                continue
            elif i == -1:
                sigm = eval(line[:line.find(' ')])
                i += 1
                continue
            if line != '\n':
                lvl = int(line[:line.find('\t')])
                if lvl < oldlvl:
                    i += 1
                    nets.append([])
                oldlvl = lvl
                n = int(line[
                    line.find('\t')+1:
                    line.find('\t',line.find('\t')+1)
                    ])
                from ast import literal_eval
                links = literal_eval(line[
                    line.find('\t',line.find('\t')+1)+1:
                    line.rfind('\t')
                    ])
                bias = float(line[line.rfind('\t')+1:-1])
                nets[i].append([lvl, n, links, bias])
                
        gen = [Network(ins,
                       outs,
                       maxlevel,
                       mnpl,
                       biased,
                       sigmoid = sigm) for ii in range(i+1)]
    for i in range(len(nets)):
        for node in nets[i]:
            if node[0] != 0 and node[0] != maxlevel+1:
                gen[i].add_node(node[0])
            gen[i].node[node[0]][node[1]].links = node[2]
            gen[i].node[node[0]][node[1]].bias_weight = node[3]
    return gen, inputs, scorings, gencount, maxtime

def savenet(net, inp, scs, gencount, maxtime, savename = ''):
    if savename == '':
        savename = 'defaultname'
##    import datetime
##    savename = savename+' '+str(datetime.datetime.now()).replace(':',' ')[:-7]
    savename = random_savename()
    import os
    if not os.path.exists('saves/'+savename):
            os.makedirs('saves/'+savename)
    with open('saves/'+savename+'/net.txt','w') as f:
        f.write(str(len(net[0].node[0]))+' - Input nodes\n' # ins
                +str(len(net[0].node[-1]))+' - Output nodes\n' #outs
                +str(len(net[0].node)-2)+' - Amount of hidden layers\n' #maxlevel-2
                +str(net[0].mnpl)+' - Max nodes per level\n'
                +str(net[0].biased)+' - Bias node interference\n'
                +str(net[0]._actfunc.__name__ == '_sigmoid')+' - Sigmoid activation function\n')
        for ne in net:
            for lvl in range(len(ne.node)):
                for n in range(len(ne.node[lvl])):
                    f.write(str(lvl)+'\t'
                            +str(n)+'\t'
                            +str(ne.node[lvl][n].links)+'\t'
                            +str(ne.node[lvl][n].bias_weight)+'\n')
    with open('saves/'+savename+'/inputs.txt','w') as f:
        for inpt in inp:
            f.write(inpt+'\n')
    with open('saves/'+savename+'/scorings.txt','w') as f:
        for inpt in scs:
            f.write(inpt+'\n')
    with open('saves/'+savename+'/generation.txt','w') as f:
        f.write(str(gencount)+'\n')
        f.write(str(maxtime)+'\n')
