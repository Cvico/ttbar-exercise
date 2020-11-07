# -*- coding: utf-8 -*-
#==============================================
# Clase para generar un canvas personalizado
#

import ROOT as r
from Selector import Selector
import Functions as F

r.gROOT.SetBatch(1)
class canvases:
    ### Constructor
    def __init__(self):
        print ('[INFO] Canvas creado correctamente')
        #Devolvemos el objeto de la clase Canvas ya configurado
        self.CreaCanvas()
        return 
        
    ### ================================
    ### Atributos
    c = r.TCanvas()
    Cname = "C1"
    topx = 10
    topy = 10
    ww = 1000
    wh = 800
    nPads = 1
    grid = True
    topMargin = 0.1
    bottomMargin = 0.02
    logY = False
    legend = r.TLegend()

    
    ### ============= Si queremos crear un pad divido en 2
    p1_mx1, p1_my1, p1_mx2, p1_my2 = 0, 0.35, 1, 0.95
    p2_mx1, p2_my1, p2_mx2, p2_my2 = 0, 0.1, 1, 0.35
    
    #=====================================================
    ### ================================
    ### Métodos
    
    def SetName(self, Cname):
        #Nombre del canvas
        self.Cname = Cname
        return 
    
    def Update(self):
        self.c.Update()
        return 
    def GetCanvas(self):
        # Nos devuelve el objeto de la clase TCanvas con los parámetros que se hayan establecido
        return self.c
    
    def GetLegend(self):
        return self.legend
    
    def SetCanvasSize(self, topx, topy, ww, wh):
        #Dimensiones establecidas para el canvas
        self.topx = topx
        self.topy = topy
        self.ww = ww
        self.wh = wh
        return
    
    def SetNpads(self, nPads):
        #Número de pads que debe tener nuestro canvas
        self.nPads = nPads
        return
    
    def SetLogY(self, boolOpt):
        ### boolOpt es True o False en función de que queramos cambiar la escala del pad
        self.logY = boolOpt
        
    def CreaCanvas(self):
        #Creamos un objeto de la clase TCanvas y lo guardamos como atributo de esta clase
        #con los parámetros que queramos
        self.c = r.TCanvas('c_' + self.Cname, 'c', self.topx, self.topy, self. ww, self.wh)
        return 
    
    def legendSetTextSize(self, LegendTextSize = 0.035):
        self.legend.SetTextSize(LegendTextSize)
        return
    
    def legendSetBorderSize(self, BorderSize = 0):
        self.legend.SetBorderSize(BorderSize)
        return
    
    def legendSetFillColor(self, color = 10):
        self.legend.SetFillColor(color)
        return
    
    def CreateLegend(self, fLegX1, fLegY1, fLegX2, fLegY2):
        self.legend = r.TLegend(fLegX1, fLegY1, fLegX2, fLegY2)
        
        self.legendSetBorderSize()
        self.legendSetFillColor()
        self.legendSetTextSize()
        
        return

    def AddEntry(self, h, name = "", option = 'f'):
        #Si h es un THStack-> name tiene que contener
        #objetos de tipo selector para extraer sus nombres
        if (isinstance(h, r.TList)):
            counter = 0
            for hist in h:
                self.AddEntry(hist, name[counter].name)
                counter += 1
            return 
        self.legend.AddEntry(h, name, option)
        return
        return 
    
    def MakeCanvas1Pad(self):
        if self.grid: self.c.SetGrid()
        return 
        
    def MakeCanvas2Pad(self):
        
        self.c.Divide(1,2)
        
        p1 = self.c.GetPad(1)
        
        p1.SetPad(self.p1_mx1, self.p1_my1, self.p1_mx2, self.p1_my2)
        p1.SetTopMargin(self.topMargin)
        p1.SetBottomMargin(self.bottomMargin)
        
        p2 = self.c.GetPad(2)
        p2.SetPad(self.p2_mx1, self.p2_my1, self.p2_mx2, self.p2_my2)
        p2.SetTopMargin(0.02)
        p2.SetBottomMargin(0.2)
        
        if self.grid: 
            p1.SetGrid()
            p2.SetGrid()
        return 
    
