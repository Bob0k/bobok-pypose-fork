
def CoefGet():
    coef = list()
    with open("coefficients.txt") as f:
        for line in f:
            coef.append(float(line[line.rfind('\t')+1:-1]))
    return coef

def MNK(x,y):

    n = min(len(x),len(y))
    n1 = 0.0
    for i in range(n):
        n1 += x[i]*x[i]
    n2 = 0.0
    for i in range(n):
        n2 += x[i]
    n3 = 0.0
    for i in range(n):
        n3 += x[i]*y[i]
    n4 = 0.0
    for i in range(n):
        n4 += y[i]
    
    b = (n3-n4*n1/n2)/(n2-n*n1/n2)
    a = (n4 - b*n)/n2
    
    return a, b
