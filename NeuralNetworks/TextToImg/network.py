#  [a1,  a2,  a3,  ..., an]
#                            *
# [[w11, w12, w13, ..., w1m],
#  [w21, w22, w23, ..., w2m],
#  [w31, w32, w33, ..., w3m],
#            ...
#  [wn1, wn2, wn3, ..., wnm]]
#                            =
#  [b1,  b2,  b3,  ..., bm]
#   b1 = a1 * w11 + a2 * w21 + a3 * w31 + ... + an * wn1
#   b2 = a1 * w12 + a2 * w22 + a3 * w32 + ... + an * wn2
#   b3 = a1 * w13 + a2 * w23 + a3 * w33 + ... + an * wn3
#     ...
#   bm = a1 * w1m + a2 * w2m + a3 * w3m + ... + an * wnm

import numpy as np
import random
from PIL import Image
 
def actfunc(i):
    return min(max(0.0,i),1.0)
    #return 1 / (1 + 2.7182818284590452353602 ** (-i))

def mutate(w = None):
    if w == None:
        w = random.choice(range(len(weights)))
    i = random.choice(range(len(weights[w])))
    j = random.choice(range(len(weights[w][i])))
    c = random.choice(range(len(weights[w][i][j])))
    ii = random.choice(range(len(weights[w][i][j][c])))
    jj = random.choice(range(len(weights[w][i][j][c][ii])))
    cc = random.choice(range(len(weights[w][i][j][c][ii][jj])))
    weights[w][i][j][c][ii][jj][cc] = 10 * (2 * random.random() - 1)
    
# Read image
imagename  = '32by32'
imagealpha = np.asarray(Image.open(imagename+'.png'))
imagesize  = imagealpha.shape[0]


weightssize   = 2 # Hidden layers + 1 amount

# Alphaless image
colors = np.squeeze(np.compress([1, 1, 1], imagealpha, axis = 2)) / 255.0

# Initialization
weights = [np.zeros(colors.shape + colors.shape) for i in range(weightssize)]

def rand(i):
    return random.random()

random.seed(2)
weights = np.vectorize(rand)(weights)

np.save('weights seed 2',weights)

#weights = np.load('weights seed 1.npy')

for i in range(weightssize):
    for j in range(imagesize):
        for k in range(imagesize):
            for c in range(3):
                weights[i][j][k][c][j][k][c] = 1
                
level = colors
for i in range(len(weights)):
    level = np.vectorize(actfunc)(level)
    level = np.tensordot(level, weights[i], axes = 3)
colors = level
    
image = level

newimage = Image.fromarray(
    np.uint8(
        np.concatenate(
            (
                image,
                np.ones((imagesize, imagesize, 1))
                ), axis = 2
            ) * 255
        )
    )
             
newimage.save(imagename + 'output2.png')
##print(newimage)
