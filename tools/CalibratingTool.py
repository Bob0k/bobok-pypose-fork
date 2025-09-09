#!/usr/bin/env python
import wx
from ToolPane import ToolPane

###############################################################################
# Sequence editor window
class CalibratingTool(ToolPane):
    """ Coefficients calibrating """

    CL_SAVE=wx.NewId()
    CL_RESET=wx.NewId()

    def __init__(self, parent, port=None):
        ToolPane.__init__(self, parent, port)

        vbox = wx.BoxSizer(wx.VERTICAL)
        
        sizer = wx.GridSizer(rows=32, cols=10, hgap=5, vgap=5)

        self.text_ctrl = list()
        self.name = list()
        
        with open("coefficients.txt") as f:
            for line in f:
                self.name.append(line[line.find('\t')+1:line.rfind('\t')])
                coef = line[line.rfind('\t')+1:-1]
                text = wx.StaticText(self, -1, self.name[-1])
                self.text_ctrl.append(wx.TextCtrl(self,-1,coef))
                sizer.Add(text, 0, wx.EXPAND)
                sizer.Add(self.text_ctrl[-1], 0, wx.EXPAND)

        vbox.Add(sizer, proportion = 1, flag = wx.EXPAND)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        okButton = wx.Button(self, self.CL_SAVE, 'Save')
        resetButton = wx.Button(self, self.CL_RESET, 'Reset')
        
        hbox.Add(okButton, proportion = 1, flag = wx.EXPAND)
        hbox.Add(resetButton, proportion = 1, flag = wx.EXPAND)
        
        vbox.Add(hbox, proportion=0, flag=wx.ALIGN_CENTER)
        self.SetSizer(vbox)
        
        wx.EVT_BUTTON(self, self.CL_SAVE, self.savef) 
        wx.EVT_BUTTON(self, self.CL_RESET, self.reset)
        
    def save(self):
        pass
    
    def savef(self,e=None):
        with open("coefficients.txt",'w') as f:
            for i in range(len(self.text_ctrl)):
                f.write(str(i)+"\t"+self.name[i]+"\t"+self.text_ctrl[i].GetValue()+"\n")
        print("Coefficients saved *clown emoji*")
        
    def reset(self,e=None):
        with open("coefficientsdefault.txt") as f:
            i = 0
            for line in f:
                if line != '\n':
                    self.text_ctrl[i].SetValue(line[line.rfind('\t')+1:-1])
                    i += 1
        print("Coefficients reset *skull emoji*")
        pass
    
NAME = "Calibrating tool"
STATUS = "coefficients edit..."
