#This is where all the extra methods used by the mini -framework are stored.

import os
from copy import deepcopy
import ROOT as r


### =============================================
### For reading the .txt
def LoadTxtFile(fName):
    #Leemos el archivo donde estan almacenadas las opciones del plotter
    f = open(fName, 'r')
    #La primera linea que lee es la ruta donde leer la rootfile que contiene los histogramas
    txt = f.readlines()
    Lines = []
    n = 0 #numero de lineas que se estan leyendo
    for Line in txt:
        if Line[0] == '#': continue
        Line = Line.split(':') #Primero eliminamos la separacion en :
        for i in range(len(Line)):
            Line[i] = LineSplitting(Line[i],'\n')
            Line[i] = LineSplitting(Line[i],' ')
            Line[i] = LineSplitting(Line[i],'\t')
        Lines.append(Line)
    f.close()
    return Lines
    
def LineSplitting(L, splits):
    #Esta funcion devuelve la linea splitteada con la informacion que nos interesa
    Lsplit = L.split(splits)
    #Al hacer el split todo lo que no contiene caracteres basicos se convierte en ''
    if splits == ' ': splits = ''
    if splits == '\t': splits = ''
    for i in range(len(Lsplit)):
        if Lsplit[i] == splits: continue
        else:
            return Lsplit[i]
    return L

def create_folder(path):
    if not os.path.exists(path): os.system("mkdir -p " + path)
    return

def GetRatioGraphUnc(h_ratio):
    nbins = h_ratio.GetNbinsX()
    x = []
    y = []
    up_unc = []
    low_unc = []
    for i in range(nbins):
        up_unc.append(h_ratio.GetBinErrorUp(i))
        low_unc.append(h_ratio.GetBinErrorLow(i))
        x.append(h_ratio.GetBin(i))
        y.append(1)
    
    gr = r.TGraphErrors(nbins, x, y, up_unc, low_unc)
    gr.SetFillColor(7)
    gr.SetLineColor(0)
    return gr

def GetRatioHist(hdata, h_expected, name, xtitle):
    #Get (data)/expected if data given
    h_ratio =  deepcopy(hdata.Clone("h_ratio"))
    h_ratio.SetMarkerStyle(20)
    h_ratio.Divide(h_expected)
    if xtitle != '':
        h_ratio.GetXaxis().SetTitle(xtitle)
        h_ratio.GetXaxis().SetLabelSize(0.1)
        h_ratio.GetXaxis().SetTitleSize(0.08)
            
    if name == 'Njet' or name == 'NbJets':
        for i in range(h_ratio.GetNbinsX()):
            h_ratio.GetXaxis().SetBinLabel(i+1, "%d"%i)
            
    if name == 'NandBjetsCompare':
        h_ratio.GetXaxis().SetBinLabel(1, "(1,0)")
        h_ratio.GetXaxis().SetBinLabel(2, "(1,1)")
        h_ratio.GetXaxis().SetBinLabel(3, "(2,0)")
        h_ratio.GetXaxis().SetBinLabel(4, "(2,1)")
        h_ratio.GetXaxis().SetBinLabel(5, "(3,0)")
        h_ratio.GetXaxis().SetBinLabel(6, "(3,1)") 
        h_ratio.GetXaxis().SetBinLabel(7, "(4,0)")
        h_ratio.SetMaximum(h_ratio.GetMaximum()*1.2)
        h_ratio.SetMinimum(h_ratio.GetMinimum()*1.2)
        h_ratio.GetYaxis().SetTitleOffset(0.6)
        h_ratio.GetYaxis().SetTitleSize(0.09)
        h_ratio.GetYaxis().SetLabelSize(0.07)
        h_ratio.GetYaxis().CenterTitle(True) #Center the text in the axis   
        
    h_ratio.GetYaxis().SetTitleSize(0.08) 
    h_ratio.GetYaxis().SetTitle(r'\frac{data}{expected}')   
    return h_ratio
    
