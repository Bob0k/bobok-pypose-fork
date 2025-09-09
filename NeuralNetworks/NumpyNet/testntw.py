import numpy as np
e = 2.7182818284590452353602

def actfunc(i):
    return 2 / (1+e**(-i)) - 1

weights = np.array(
    [[[ 0.73986673, -0.47687529,  0.30930605],
      [ 0.11064926,  0.79008942,  0.8363382 ],
      [-0.97258728, -0.86691954,  0.73801317]],
     
     [[-0.69038945,  0.59923053,  0.09277854],
      [-0.28669568, -0.30459569,  0.9549604 ],
      [-0.79580953, -0.45077284,  0.08919127]]])

inputv = np.array([1, 2, 3])
inputv = np.vectorize(actfunc)(inputv)
inputv = np.matmul(inputv, weights)
inputv = np.sum(inputv, axis = 0)
#inputv = np.vectorize(actfunc)(inputv)
print(inputv)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("""inputv = np.array([1, 2, 3])
inputv = np.vectorize(actfunc)(inputv)
inputv = np.matmul(inputv, weights)
inputv = np.sum(inputv, axis = 0)""",
                        setup = """import numpy as np
e = 2.7182818284590452353602

def actfunc(i):
    return 2 / (1+e**(-i)) - 1
weights = np.array(
    [[[ 0.73986673, -0.47687529,  0.30930605],
      [ 0.11064926,  0.79008942,  0.8363382 ],
      [-0.97258728, -0.86691954,  0.73801317]],
     
     [[-0.69038945,  0.59923053,  0.09277854],
      [-0.28669568, -0.30459569,  0.9549604 ],
      [-0.79580953, -0.45077284,  0.08919127]]])""",
                        number = 50000)/50000.0)

