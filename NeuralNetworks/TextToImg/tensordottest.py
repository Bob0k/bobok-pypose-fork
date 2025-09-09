import numpy as np

# Single color
##t0 = np.array(
##    [[1000, 100],
##     [10,   1]]
##    )
##w0 = np.array([[
##    [[1, 1],
##     [1, 1]],
##    [[2, 2],
##     [2, 2]]],
##    [[[3, 3],
##     [3, 3]],
##    [[4, 4],
##     [4, 4]]
##    ]]
##    )
##tw = np.tensordot(t0, w0, axes = 2)

### Several colours
##t0 = np.ones((4, 4, 3))
##w0 = np.ones((4, 4, 3, 4, 4, 3))
##
##tw = np.tensordot(t0, w0, axes = 3)
##
##print(tw)

#Dimention change
inittensorshape = ()
inittensor = np.ones(inittensorshape)

targettensorshape = (32, 32, 3)
weights = np.ones(
    inittensorshape + targettensorshape
    )

targettensor = np.tensordot(inittensor, weights, axes = len(inittensorshape))

print(targettensor.shape)
