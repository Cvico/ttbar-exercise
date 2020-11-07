# -*- coding: utf-8 -*-
from canvases import canvases as cv
import ROOT as r

f1 = r.TFile.Open("files/ttbar.root")
f2 = r.TFile.Open("files/dy.root")


t1 = f1.events
t2 = f2.events




micanvas = cv() #Creamos el objeto de clase canvases
micanvas.MakeCanvas2Pad()
micanvas.SetName("prueba")

c = micanvas.GetCanvas()
p1 = c.GetPad(1)
p1.cd()
t1.Draw("EventWeight")

p2 = c.GetPad(2)
p2.SetLogy()

p2.cd()
t2.Draw("NJet")

c.Print('prueba.png', 'png')



