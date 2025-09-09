name = list()
coef = list()

with open("coefficients.txt") as f:
    for line in f:
        name.append(line[line.find('\t')+1:line.rfind('\t')])
        coef.append(float(line[line.rfind('\t')+1:-1]))
for i in range(len(coef)):
    print(name[i]+' - '+str(coef[i]))
