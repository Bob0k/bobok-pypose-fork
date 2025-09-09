import numpy as np
from PIL import Image
import random

def actfunc(i):
    #return min(max(0.0,i),1.0)
    return 1 / (1 + 2.7182818284590452353602 ** (-i))

def rand(i):
    return random.random()

# User Input
prompt    = float(input("Please input prompt: "))
seed      = int(input("Please input seed: "))
imagesize = max(1,min(int(input("Please input image size: ")),31))
weightssize = 1

random.seed(seed)
imageshape = (imagesize, imagesize, 3)
inweight = np.vectorize(rand)(
    np.empty(imageshape)
    )
weights = [np.empty(imageshape + imageshape) for i in range(weightssize)]
for i in range(weightssize):
    weights[i] = np.vectorize(rand)(weights[i])
level = np.tensordot(prompt, inweight, axes = 0)
for i in range(len(weights)):
    level = np.vectorize(actfunc)(level)
    level = np.tensordot(level, weights[i], axes = 3)

newimage = Image.fromarray(
    np.uint8(
        np.concatenate(
            (
                level,
                np.ones((imagesize, imagesize, 1))
                ), axis = 2
            ) * 255
        )
    )        
newimage.save('texttoimageoutputs/'
              + str(prompt) + ' '
              + str(seed) + ' '
              + str(imagesize) + '.png')
np.save('texttoimageweights/'
        + str(prompt) + ' '
        + str(seed) + ' '
        + str(imagesize),
        weights)     
