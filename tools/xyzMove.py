#!/usr/bin/env python
import math
import wx
import project
from ToolPane import ToolPane
from ax12 import *
from MNK import *

###############################################################################
# Sequence editor window
class xyzMove(ToolPane):
    """ Coordinate-wise movement of target block """

    BT_RUN=wx.NewId()
    BT_LOOP=wx.NewId()
    BT_HALT=wx.NewId()
    BT_SWAP=wx.NewId()

    def __init__(self, parent, port=None):
        ToolPane.__init__(self, parent, port)
        self.tranbox = []
        #coordinates input
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        wx.StaticBox(panel, -1, 'Start coordinates', (5, 5), (175, 100))
        wx.StaticText(panel, -1, 'x0:', (15,30))
        self.x0 = wx.TextCtrl(panel, -1, '150', (50,25))
        wx.StaticText(panel, -1, 'y0:', (15,55))
        self.y0 = wx.TextCtrl(panel, -1, '0', (50,50))
        wx.StaticText(panel, -1, 'z0:', (15,80))
        self.z0 = wx.TextCtrl(panel, -1, '0', (50,75))

        dist = 185
        wx.StaticBox(panel, -1, 'Goal coordinates', (5 + dist, 5), (175, 100))
        wx.StaticText(panel, -1, 'x1:', (15 + dist,30))
        self.x1 = wx.TextCtrl(panel, -1, '100', (50 + dist,25))
        wx.StaticText(panel, -1, 'y1:', (15 + dist,55))
        self.y1 = wx.TextCtrl(panel, -1, '0', (50 + dist,50))
        wx.StaticText(panel, -1, 'z1:', (15 + dist,80))
        self.z1 = wx.TextCtrl(panel, -1, '0', (50 + dist,75))


        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, self.BT_RUN, 'Ok', size=(70, 30))
        swapButton = wx.Button(self, self.BT_SWAP, 'Swap', size=(70, 30)) 
        closeButton = wx.Button(self, self.BT_HALT, 'Halt', size=(70, 30)) 
        hbox.Add(okButton, 1)
        hbox.Add(swapButton, 1, wx.LEFT, 5)
        hbox.Add(closeButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)
           
        wx.EVT_BUTTON(self, self.BT_RUN, self.runSeq) 
        wx.EVT_BUTTON(self, self.BT_HALT, self.haltSeq)
        wx.EVT_BUTTON(self, self.BT_SWAP, self.swap)

    def swap(self, e = None):
        tempx = self.x1.GetValue()
        tempy = self.y1.GetValue()
        tempz = self.z1.GetValue()
    
        self.x1.SetValue(self.x0.GetValue())
        self.y1.SetValue(self.y0.GetValue())
        self.z1.SetValue(self.z0.GetValue())
        
        self.x0.SetValue(tempx)
        self.y0.SetValue(tempy)
        self.z0.SetValue(tempz)
        
    def save(self):
        if len(self.tranbox) > 0:
            self.parent.project.sequences["xyz"] = project.sequence()
            for i in range(len(self.tranbox)):
                self.parent.project.sequences["xyz"].append(self.tranbox[i].replace(",","|"))               
        self.parent.project.save = True

    def runSeq(self, e=None):
        """ Add 8 xyz poses. """
        if self.parent.project.name != "":
            for i in range(8):
                self.parent.project.poses["xyz"+str(i+1)] = project.pose("",self.parent.project.count)
            self.parent.project.poses["default"] = project.pose("",self.parent.project.count)


    #MNK and other stuff
            ro0 = 0
            psi0 = 0
            h0 = 0
            ro1 = 0
            psi1 = 0
            h1 = 0

            ro0 = math.sqrt(float(self.x0.GetValue())**2 + float(self.y0.GetValue())**2)
            if (float(self.x0.GetValue()) == 0):
                psi0 = 1.5707963267948965 * float(self.y0.GetValue())/abs(float(self.y0.GetValue()))
            elif (float(self.x0.GetValue()) > 0):
                psi0 = math.atan(float(self.y0.GetValue())/float(self.x0.GetValue()))
            else:
                if (float(self.y0.GetValue()) >= 0): 
                    psi0 = 3.1415926535897932 - math. atan(-float(self.y0.GetValue())/float(self.x0.GetValue()))
                else:
                    psi0 = -3.1415926535897932 + math.atan(float(self.y0.GetValue())/float(self.x0.GetValue()))
            h0 = float(self.z0.GetValue())

            ro1 = math.sqrt(float(self.x1.GetValue())**2 + float(self.y1.GetValue())**2)
            if (float(self.x1.GetValue()) == 0):
                psi1 = 1.5707963267948965 * float(self.y1.GetValue())/abs(float(self.y1.GetValue()))
            elif (float(self.x1.GetValue()) > 0):
                psi1 = math.atan(float(self.y1.GetValue())/float(self.x1.GetValue()))
            else:
                if (float(self.y1.GetValue()) >= 0): 
                    psi1 = 3.1415926535897932 - math.atan(-float(self.y1.GetValue())/float(self.x1.GetValue()))
                else:
                    psi1 = -3.1415926535897932 + math.atan(float(self.y1.GetValue())/float(self.x1.GetValue()))
            h1 = float(self.z1.GetValue())

            coef = CoefGet()

            # Poses and IRL coords dependence:
            # y = ki * x + bi   <=> IRL = ki * pos + bi
            # x = (y - bi) / ki <=> pos = (IRL - bi) / ki
            k1, b1 = MNK([coef[72],coef[73],coef[74],coef[75],coef[76]],
                         [coef[77]/57.29578,
                          coef[78]/57.29578,
                          coef[79]/57.29578,
                          coef[80]/57.29578,
                          coef[81]/57.29578])


            # Distance and poses dependence:
            # y = ki * x + bi <=> pos = ki * DIS(ro) + bi        
            k2on0, b2on0 = MNK([50,100,150,200,250,300],
                [coef[0],coef[1],coef[2],coef[3],coef[4],coef[5]]
                )
            k4on0, b4on0 = MNK([50,100,150,200,250,300],
                [coef[6],coef[7],coef[8],coef[9],coef[10],coef[11]])
            k6on0, b6on0 = MNK([50,100,150,200,250,300],
                [coef[12],coef[13],coef[14],coef[15],coef[16],coef[17]])

            k2at0, b2at0 = MNK([50,100,150,200,250,300],
                [coef[18],coef[19],coef[20],coef[21],coef[22],coef[23]])
            k4at0, b4at0 = MNK([50,100,150,200,250,300],
                [coef[24],coef[25],coef[26],coef[27],coef[28],coef[29]])
            k6at0, b6at0 = MNK([50,100,150,200,250,300],
                [coef[30],coef[31],coef[32],coef[33],coef[34],coef[35]])

            k2on93, b2on93 = MNK([50,100,150,200,250,300],
                [coef[36],coef[37],coef[38],coef[39],coef[40],coef[41]]
                )
            k4on93, b4on93 = MNK([50,100,150,200,250,300],
                [coef[42],coef[43],coef[44],coef[45],coef[46],coef[47]])
            k6on93, b6on93 = MNK([50,100,150,200,250,300],
                [coef[48],coef[49],coef[50],coef[51],coef[52],coef[53]])

            k2at93, b2at93 = MNK([50,100,150,200,250,300],
                [coef[54],coef[55],coef[56],coef[57],coef[58],coef[59]])
            k4at93, b4at93 = MNK([50,100,150,200,250,300],
                [coef[60],coef[61],coef[62],coef[63],coef[64],coef[65]])
            k6at93, b6at93 = MNK([50,100,150,200,250,300],
                [coef[66],coef[67],coef[68],coef[69],coef[70],coef[71]])

            k2ons = (k2on93 - k2on0)/93*h0 + k2on0
            k4ons = (k4on93 - k4on0)/93*h0 + k4on0
            k6ons = (k6on93 - k6on0)/93*h0 + k6on0
            b2ons = (b2on93 - b2on0)/93*h0 + b2on0
            b4ons = (b4on93 - b4on0)/93*h0 + b4on0
            b6ons = (b6on93 - b6on0)/93*h0 + b6on0
        
            k2ats = (k2at93 - k2at0)/93*h0 + k2at0
            k4ats = (k4at93 - k4at0)/93*h0 + k4at0
            k6ats = (k6at93 - k6at0)/93*h0 + k6at0
            b2ats = (b2at93 - b2at0)/93*h0 + b2at0
            b4ats = (b4at93 - b4at0)/93*h0 + b4at0
            b6ats = (b6at93 - b6at0)/93*h0 + b6at0

            k2onf = (k2on93 - k2on0)/93*h1 + k2on0
            k4onf = (k4on93 - k4on0)/93*h1 + k4on0
            k6onf = (k6on93 - k6on0)/93*h1 + k6on0
            b2onf = (b2on93 - b2on0)/93*h1 + b2on0
            b4onf = (b4on93 - b4on0)/93*h1 + b4on0
            b6onf = (b6on93 - b6on0)/93*h1 + b6on0
        
            k2atf = (k2at93 - k2at0)/93*h1 + k2at0
            k4atf = (k4at93 - k4at0)/93*h1 + k4at0
            k6atf = (k6at93 - k6at0)/93*h1 + k6at0
            b2atf = (b2at93 - b2at0)/93*h1 + b2at0
            b4atf = (b4at93 - b4at0)/93*h1 + b4at0
            b6atf = (b6at93 - b6at0)/93*h1 + b6at0

            print("k2on0",k2on0)
            print("b2on0",b2on0)
            
            print("k2on93",k2on93)
            print("b2on93",b2on93)
            
            print("k2ons",k2on0)
            print("b2ons",b2on0)
            
            print("k2onf",k2onf)
            print("b2onf",b2onf)
            
            pos1start   = int((psi0 - b1) / k1)

            pos2starton = int((k2ons * ro0) + b2ons)
            pos3starton = int(1023 - pos2starton)
            pos4starton = int((k4ons * ro0) + b4ons)
            pos5starton = int(1023 - pos4starton)
            pos6starton = int((k6ons * ro0) + b6ons)

            pos2startat = int((k2ats * ro0) + b2ats)
            pos3startat = int(1023 - pos2startat)
            pos4startat = int((k4ats * ro0) + b4ats)
            pos5startat = int(1023 - pos4startat)
            pos6startat = int((k6ats * ro0) + b6ats)

            pos1finish   = int((psi1 - b1) / k1)

            pos2finishon = int((k2onf * ro1) + b2onf)
            pos3finishon = int(1023 - pos2finishon)
            pos4finishon = int((k4onf * ro1) + b4onf)
            pos5finishon = int(1023 - pos4finishon)
            pos6finishon = int((k6onf * ro1) + b6onf)

            pos2finishat = int((k2atf * ro1) + b2atf)
            pos3finishat = int(1023 - pos2finishat)
            pos4finishat = int((k4atf * ro1) + b4atf)
            pos5finishat = int(1023 - pos4finishat)
            pos6finishat = int((k6atf * ro1) + b6atf)

            pos7 = 512
            pos8n = 512
            pos8y = 240

            self.parent.project.poses["xyz1"][0] = pos1start
            self.parent.project.poses["xyz1"][1] = pos2starton
            self.parent.project.poses["xyz1"][2] = pos3starton
            self.parent.project.poses["xyz1"][3] = pos4starton
            self.parent.project.poses["xyz1"][4] = pos5starton
            self.parent.project.poses["xyz1"][5] = pos6starton
            self.parent.project.poses["xyz1"][6] = pos7
            self.parent.project.poses["xyz1"][7] = pos8n

            self.parent.project.poses["xyz2"][0] = pos1start
            self.parent.project.poses["xyz2"][1] = pos2startat
            self.parent.project.poses["xyz2"][2] = pos3startat
            self.parent.project.poses["xyz2"][3] = pos4startat
            self.parent.project.poses["xyz2"][4] = pos5startat
            self.parent.project.poses["xyz2"][5] = pos6startat
            self.parent.project.poses["xyz2"][6] = pos7
            self.parent.project.poses["xyz2"][7] = pos8n
            
            self.parent.project.poses["xyz3"][0] = pos1start
            self.parent.project.poses["xyz3"][1] = pos2startat
            self.parent.project.poses["xyz3"][2] = pos3startat
            self.parent.project.poses["xyz3"][3] = pos4startat
            self.parent.project.poses["xyz3"][4] = pos5startat
            self.parent.project.poses["xyz3"][5] = pos6startat
            self.parent.project.poses["xyz3"][6] = pos7
            self.parent.project.poses["xyz3"][7] = pos8y

            self.parent.project.poses["xyz4"][0] = pos1start
            self.parent.project.poses["xyz4"][1] = pos2starton
            self.parent.project.poses["xyz4"][2] = pos3starton
            self.parent.project.poses["xyz4"][3] = pos4starton
            self.parent.project.poses["xyz4"][4] = pos5starton
            self.parent.project.poses["xyz4"][5] = pos6starton
            self.parent.project.poses["xyz4"][6] = pos7
            self.parent.project.poses["xyz4"][7] = pos8y
            
            self.parent.project.poses["xyz5"][0] = pos1finish
            self.parent.project.poses["xyz5"][1] = pos2finishon
            self.parent.project.poses["xyz5"][2] = pos3finishon
            self.parent.project.poses["xyz5"][3] = pos4finishon
            self.parent.project.poses["xyz5"][4] = pos5finishon
            self.parent.project.poses["xyz5"][5] = pos6finishon
            self.parent.project.poses["xyz5"][6] = pos7
            self.parent.project.poses["xyz5"][7] = pos8y

            self.parent.project.poses["xyz6"][0] = pos1finish
            self.parent.project.poses["xyz6"][1] = pos2finishat
            self.parent.project.poses["xyz6"][2] = pos3finishat
            self.parent.project.poses["xyz6"][3] = pos4finishat
            self.parent.project.poses["xyz6"][4] = pos5finishat
            self.parent.project.poses["xyz6"][5] = pos6finishat
            self.parent.project.poses["xyz6"][6] = pos7
            self.parent.project.poses["xyz6"][7] = pos8y

            self.parent.project.poses["xyz7"][0] = pos1finish
            self.parent.project.poses["xyz7"][1] = pos2finishat
            self.parent.project.poses["xyz7"][2] = pos3finishat
            self.parent.project.poses["xyz7"][3] = pos4finishat
            self.parent.project.poses["xyz7"][4] = pos5finishat
            self.parent.project.poses["xyz7"][5] = pos6finishat
            self.parent.project.poses["xyz7"][6] = pos7
            self.parent.project.poses["xyz7"][7] = pos8n
            
            self.parent.project.poses["xyz8"][0] = pos1finish
            self.parent.project.poses["xyz8"][1] = pos2finishon
            self.parent.project.poses["xyz8"][2] = pos3finishon
            self.parent.project.poses["xyz8"][3] = pos4finishon
            self.parent.project.poses["xyz8"][4] = pos5finishon
            self.parent.project.poses["xyz8"][5] = pos6finishon
            self.parent.project.poses["xyz8"][6] = pos7
            self.parent.project.poses["xyz8"][7] = pos8n
            
            self.parent.project.poses["default"][0] = int(coef[132])
            self.parent.project.poses["default"][1] = int(coef[133])
            self.parent.project.poses["default"][2] = int(coef[134])
            self.parent.project.poses["default"][3] = int(coef[135])
            self.parent.project.poses["default"][4] = int(coef[136])
            self.parent.project.poses["default"][5] = int(coef[137])
            self.parent.project.poses["default"][6] = int(coef[138])
            self.parent.project.poses["default"][7] = int(coef[139])
            
            """ create a new xyz sequence. """
            if self.parent.project.name != "":
                self.parent.project.sequences["xyz"] = project.sequence("")

            """ create transtions in this sequence. """
            self.tranbox = ["xyz1,1000",
                            "xyz2,2000",
                            "xyz3,2000",
                            "xyz4,1000",
                            "xyz5,1000",
                            "xyz6,2000",
                            "xyz7,2000",
                            "xyz8,1000",
                            "default,2500"]

            """ download poses, seqeunce, and send. """
            self.save() # save sequence            
            if self.port != None:
                print "Run sequence..."
                poseDL = dict()     # key = pose name, val = index, download them after we build a transition list
                tranDL = list()     # list of bytes to download
                for t in self.parent.project.sequences["xyz"]:  
                    p = t[0:t.find("|")]                    # pose name
                    dt = int(t[t.find("|")+1:])             # delta-T
                    if p not in poseDL.keys():
                        poseDL[p] = len(poseDL.keys())      # get ix for pose
                    # create transition values to download
                    tranDL.append(poseDL[p])                # ix of pose
                    tranDL.append(dt%256)                   # time is an int (16-bytes)
                    tranDL.append(dt>>8)
                tranDL.append(255)      # notice to stop
                tranDL.append(0)        # time is irrelevant on stop    
                tranDL.append(0)
                # set pose size -- IMPORTANT!
                print "Setting pose size at " + str(self.parent.project.count)
                self.port.execute(253, 7, [self.parent.project.count])
                # send poses            
                for p in poseDL.keys():
                    print "Sending pose " + str(p) + " to position " + str(poseDL[p])
                    self.port.execute(253, 8, [poseDL[p]] + project.extract(self.parent.project.poses[p])) 
                print "Sending sequence: " + str(tranDL)
                # send sequence and play            
                self.port.execute(253, 9, tranDL) 
                # run or loop?
                if e.GetId() == self.BT_LOOP:
                    self.port.execute(253,11,list())
                else:
                    self.port.execute(253, 10, list())
                self.parent.sb.SetStatusText('Playing Sequence: ' + "xyz")
            else:
                self.parent.sb.SetBackgroundColour('RED')
                self.parent.sb.SetStatusText("No Port Open",0) 
                self.parent.timer.Start(20)

            """ remove a sequence. """


            # this order is VERY important!

            del self.parent.project.sequences["xyz"]

            """ Removing xyzi poses. """
            for i in range(8):
                del self.parent.project.poses["xyz"+str(i+1)]
                
            self.save() # save sequence      
        else:
            dlg = wx.MessageDialog(self, 'Please create a new robot first.', 'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
        

    def haltSeq(self, e=None):
        """ send halt message ("H") """ 
        if self.port != None:
            print "Halt sequence..."
            self.port.ser.write("H")
        else:
            self.parent.sb.SetBackgroundColour('RED')
            self.parent.sb.SetStatusText("No Port Open",0) 
            self.parent.timer.Start(20)

NAME = "xyz Move"
STATUS = "please create or select a sequence to edit..."
