import math

ro0 = 0
psi0 = 0
h0 = 0
ro1 = 0
psi1 = 0
h1 = 0

x0 = 150
y0 = 0
z0 = 0
x1 = 150
y1 = 75
z1 = 0

ro0 = math.sqrt(float(x0)**2 + float(y0)**2)
if (float(x0) == 0):
    psi0 = 1.5707963267948965 * float(y0)/abs(float(y0))
elif (float(x0) > 0):
    psi0 = math.atan(float(y0)/float(x0))
else:
    if (float(y0) >= 0): 
        psi0 = 3.1415926535897932 - math.atan(-float(y0)/float(x0))
    else:
        psi0 = -3.1415926535897932 + math.atan(float(y0)/float(x0))
h0 = float(z0)

ro1 = math.sqrt(float(x1)**2 + float(y1)**2)
if (float(x1) == 0):
    psi1 = 1.5707963267948965 * float(y1)/abs(float(y1))
elif (float(x1) > 0):
    psi1 = math.atan(float(y1)/float(x1))
else:
    if (float(y1) >= 0): 
        psi1 = 3.1415926535897932 - math.atan(-float(y1)/float(x1))
    else:
        psi1 = -3.1415926535897932 + math.atan(float(y1)/float(x1))
h1 = float(z1)

print([ro0,psi0*180/3.1415926535897932,h0,ro1,psi1*180/3.1415926535897932,h1])

#name = list()
coef = list()

with open("coefficients.txt") as f:
    for line in f:
        #name.append(line[line.find('\t')+1:line.rfind('\t')])
        coef.append(float(line[line.rfind('\t')+1:-1]))

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

# Poses and IRL coords dependence:
# y = ki * x + bi   <=> IRL = ki * pos + bi
# x = (y - bi) / ki <=> pos = (IRL - bi) / ki
print(coef[77])
k1, b1 = MNK([coef[68],coef[69],coef[70],coef[71],coef[72]],
             [coef[73]/57.29578,
              coef[74]/57.29578,
              coef[75]/57.29578,
              coef[76]/57.29578,
              coef[77]/57.29578])
print(k1,b1)

k2, b2 = MNK([coef[1],coef[7]],[coef[13],coef[19]])
k4, b4 = MNK([coef[2],coef[8]],[coef[14],coef[20]])
k6, b6 = MNK([coef[3],coef[9]],[coef[15],coef[21]])
k7, b7 = MNK([coef[4],coef[10]],[coef[16],coef[22]])
k8, b8 = MNK([coef[5],coef[11]],[coef[17],coef[23]])

# Distance and poses dependence:
# y = ki * x + bi <=> pos = ki * DIS(ro) + bi        
k2on, b2on = MNK([50,100,150,200,250,300],
    [coef[24],coef[25],coef[26],coef[27],coef[28],coef[29]]
    )
k4on, b4on = MNK([50,100,150,200,250,300],
    [coef[30],coef[31],coef[32],coef[33],coef[34],coef[35]])
k6on, b6on = MNK([50,100,150,200,250,300],
    [coef[36],coef[37],coef[38],coef[39],coef[40],coef[41]])

k2at, b2at = MNK([50,100,150,200,250,300],
    [coef[42],coef[43],coef[44],coef[45],coef[46],coef[47]])
k4at, b4at = MNK([50,100,150,200,250,300],
    [coef[48],coef[49],coef[50],coef[51],coef[52],coef[53]])
k6at, b6at = MNK([50,100,150,200,250,300],
    [coef[54],coef[55],coef[56],coef[57],coef[58],coef[59]])

pos1start   = int((psi0 - b1) / k1)

pos2starton = int((k2on * ro0) + b2on)
pos3starton = int(1023 - pos2starton)
pos4starton = int((k4on * ro0) + b4on)
pos5starton = int(1023 - pos4starton)
pos6starton = int((k6on * ro0) + b6on)

pos2startat = int((k2at * ro0) + b2at)
pos3startat = int(1023 - pos2startat)
pos4startat = int((k4at * ro0) + b4at)
pos5startat = int(1023 - pos4startat)
pos6startat = int((k6at * ro0) + b6at)

pos1finish   = int((psi1 - b1) / k1)

pos2finishon = int((k2on * ro1) + b2on)
pos3finishon = int(1023 - pos2finishon)
pos4finishon = int((k4on * ro1) + b4on)
pos5finishon = int(1023 - pos4finishon)
pos6finishon = int((k6on * ro1) + b6on)

pos2finishat = int((k2at * ro1) + b2at)
pos3finishat = int(1023 - pos2finishat)
pos4finishat = int((k4at * ro1) + b4at)
pos5finishat = int(1023 - pos4finishat)
pos6finishat = int((k6at * ro1) + b6at)

pos7 = 512
pos8n = 512
pos8y = 240

print(pos1start," = pos1start")
print(pos2starton," = pos2starton")
print(pos3starton," = pos3starton")
print(pos4starton," = pos4starton")
print(pos5starton," = pos5starton")
print(pos6starton," = pos6starton")

print(pos2startat," = pos2startat")
print(pos3startat," = pos3startat")
print(pos4startat," = pos4startat")
print(pos5startat," = pos5startat")
print(pos6startat," = pos6startat")

print(pos1finish," = pos1finish")

print(pos2finishon," = pos2finishon")
print(pos3finishon," = pos3finishon")
print(pos4finishon," = pos4finishon")
print(pos5finishon," = pos5finishon")
print(pos6finishon," = pos6finishon")

print(pos2finishat," = pos2finishat")
print(pos3finishat," = pos3finishat")
print(pos4finishat," = pos4finishat")
print(pos5finishat," = pos5finishat")
print(pos6finishat," = pos6finishat")


with open("xyz.ppr",'w') as f:
    f.write("Test:8:1024:1024:1024:1024:1024:1024:1024:1024"+'\n'+
            "Pose=default:488, 287, 731, 317, 707, 509, 510, 510"+'\n'+
            "Pose=xyz1:"+str(pos1start)+", "+str(pos2starton)+", "+str(pos3starton)+", "+str(pos4starton)+", "+str(pos5starton)+", "+str(pos6starton)+", "+str(pos7)+", "+str(pos8n)+'\n'+
            "Pose=xyz2:"+str(pos1start)+", "+str(pos2startat)+", "+str(pos3startat)+", "+str(pos4startat)+", "+str(pos5startat)+", "+str(pos6startat)+", "+str(pos7)+", "+str(pos8n)+'\n'+
            "Pose=xyz3:"+str(pos1start)+", "+str(pos2startat)+", "+str(pos3startat)+", "+str(pos4startat)+", "+str(pos5startat)+", "+str(pos6startat)+", "+str(pos7)+", "+str(pos8y)+'\n'+
            "Pose=xyz4:"+str(pos1start)+", "+str(pos2starton)+", "+str(pos3starton)+", "+str(pos4starton)+", "+str(pos5starton)+", "+str(pos6starton)+", "+str(pos7)+", "+str(pos8y)+'\n'+
            "Pose=xyz5:"+str(pos1finish)+", "+str(pos2finishon)+", "+str(pos3finishon)+", "+str(pos4finishon)+", "+str(pos5finishon)+", "+str(pos6finishon)+", "+str(pos7)+", "+str(pos8y)+'\n'+
            "Pose=xyz6:"+str(pos1finish)+", "+str(pos2finishat)+", "+str(pos3finishat)+", "+str(pos4finishat)+", "+str(pos5finishat)+", "+str(pos6finishat)+", "+str(pos7)+", "+str(pos8y)+'\n'+
            "Pose=xyz7:"+str(pos1finish)+", "+str(pos2finishat)+", "+str(pos3finishat)+", "+str(pos4finishat)+", "+str(pos5finishat)+", "+str(pos6finishat)+", "+str(pos7)+", "+str(pos8n)+'\n'+
            "Pose=xyz8:"+str(pos1finish)+", "+str(pos2finishon)+", "+str(pos3finishon)+", "+str(pos4finishon)+", "+str(pos5finishon)+", "+str(pos6finishon)+", "+str(pos7)+", "+str(pos8n)+'\n'+
            "Seq=xyz: xyz1|500, xyz2|2000, xyz3|2000, xyz4|500, xyz5|500, xyz6|2000, xyz7|2000, xyz8|1500, default|1500\n")
