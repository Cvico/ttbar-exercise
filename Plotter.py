# -*- coding: utf-8 -*-
import warnings as wr
from Selector import Selector
import ROOT as r
from copy import deepcopy
import Functions as F

class Plotter:
    ''' Class to draw histograms and get info from Selector'''
    ### =============================================
    ### Constructor
    def __init__(self, processes, hist_list, colors):
        ''' Initialize a new plotter... give a list with all names of MC samples and the name of the data sample '''
        #self.ResetVariables()

        for p in processes:
            if processes[p] == "data": self.data = Selector(hist_list,processes[p])
            elif "+" in process[p]: self.signal = Selector(hist_list,processes[p])
            else: self.backgrounds.append(Selector(hist_list,processes[p]))
        
        return


    ### =============================================
    ### Atributos de configuracion
    processess = ""
    hist_list = []
    savepath = "."
    backgrounds = []
    data = ''
    colors = []
    Annotations = []
    Histos = []
    
    ### Parametros por defecto para los plots
    fLegX1, fLegY1, fLegX2, fLegY2 = 0.75, 0.55, 0.89, 0.89
    p1_mx1, p1_my1, p1_mx2, p1_my2 = 0, 0.35, 1, 0.95
    p2_mx1, p2_my1, p2_mx2, p2_my2 = 0, 0.1, 1, 0.35
    topMargin = 0.1
    bottomMargin = 0.02
    topx = 10
    topy = 10
    ww = 1000
    wh = 800
    LegendTextSize  = 0.035
    xtitle = ''
    ytitle = ''
    title  = ''
    LogY = False
    compareTrigg = False
    
    ### =============================================
    ### Methods
    def SetLegendPos(self, x1, y1, x2, y2):
        ''' Change the default position of the legend'''
        self.fLegX1 = x1
        self.fLegY1 = y1
        self.fLegX2 = x2
        self.fLegY2 = y2
                
    
    def SetLegendSize(self, t = 0.065):
        ''' Change the default size of the text in the legend'''
        self.LegendTextSize = t


    def SetSavePath(self, newpath):
        '''Change where plots and text dumps are going to be saved. By default: ./results'''
        self.savepath = newpath


    def SetColors(self, col):
        ''' Set the colors for each MC sample '''
        self.colors = col

    def SetAnnotations(self, Annotations):
        ''' Set Annotations for the plot '''
        self.Annotations = Annotations

    def SetTitle(self, tit):
        ''' Set title of the plot '''
        self.title = tit


    def SetXtitle(self, tit):
        ''' Set title of X axis '''
        self.xtitle = tit


    def SetYtitle(self, tit):
        ''' Set title of Y axis '''
        self.ytitle = tit
   
    def SetLogScale(self):
        self.LogY = True

    def SetLinearScale(self):
        self.LogY = False

    def GetHisto(self, process, name):
        ''' Returns histogram 'name' for a given process '''
        for s in self.listOfSelectors:
            if name not in s.name: continue
            h = s.GetHisto(name)
            return h

        wr.warn("[Plotter::GetHisto] WARNING: histogram {h} for process {p} not found!".format(h = name, p = process))
        return r.TH1F()


    def GetEvents(self, process, name):
        ''' Returns the integral of a histogram '''
        return self.GetHisto(process, name).Integral()

    def GetSampleName(self, name):
        for s in self.listOfSelectors:
            if s.GetSampleName() == name: 
                return s
            
    def CreateCommentBox(self, x0, y0, x1, y1, color):
        #Bbox for remarking efficiency zones
        #print('Drawing TBox')
        bbox = r.TBox(x0, y0, x1, y1)
        bbox.SetFillColorAlpha(color, 0.3)
        return bbox
    
    def Annotate(self, x, y, text):
        H = r.TLatex() #header
        H.SetNDC()
        H.SetTextSize(0.07)
        H.DrawLatex(x, y, text)
    

    
    def GetStackedHistos(self, name):
        hstack = r.THStack('hstack_' + name, "hstack")
        
        counter = 0
        for s in self.listOfSelectors:
            h = s.GetHisto(name)
            h.SetFillColor(self.colors[counter])
            h.SetLineColor(0)
            hstack.Add(h)
            counter += 1
        
        return hstack
    
    def MakeCanvas2Pad(self, name):
        c = r.TCanvas('c_' + name, '', self.topx, self.topy, self.ww, self.wh)
        c.Divide(1,2)
        
        p1 = c.GetPad(1)
        
        p1.SetPad(self.p1_mx1, self.p1_my1, self.p1_mx2, self.p1_my2)
        p1.SetTopMargin(self.topMargin)
        p1.SetBottomMargin(self.bottomMargin)
        
        p2 = c.GetPad(2)
        p2.SetPad(self.p2_mx1, self.p2_my1, self.p2_mx2, self.p2_my2)
        p2.SetTopMargin(0.02)
        p2.SetBottomMargin(0.2)
        
         
        p1.SetGrid()
        p2.SetGrid()
        
        return c     
    
    def CreateLegend(self):        
        legend = r.TLegend(self.fLegX1, self.fLegY1, self.fLegX2, self.fLegY2)
        
        legend.SetBorderSize(0)
        legend.SetFillColor(10)
        legend.SetTextSize(0.035)

        return legend
    
    def AddEntry(self, h, legend, name = "", option = 'f'):
        #Si h es un THStack-> name tiene que contener
        #objetos de tipo selector para extraer sus nombres
        if (isinstance(h, r.TList)):
            counter = 0
            for hist in h:
                self.AddEntry(hist, legend, name[counter].name)
                counter += 1
            return 
        
        legend.AddEntry(h, name, option)
        return
    
    def GetExpectedHist(self, name):
        nbins = self.listOfSelectors[0].GetHisto(name).GetNbinsX()
        xlow = self.listOfSelectors[0].GetHisto(name).GetXaxis().GetXmin()
        xup = self.listOfSelectors[0].GetHisto(name).GetXaxis().GetXmax()
        
        h_expected = r.TH1F('h_expected_' + name, '', nbins, xlow, xup) #Copy the structure of one of the 
        h_expected.SetFillStyle(3345)
        h_expected.SetMarkerStyle(0)
        h_expected.SetFillColor(r.kBlack)
        h_expected.SetLineColor(0)
        counter = 0
        for s in self.listOfSelectors:
            h = s.GetHisto(name)
            h_expected.Add(h, 1)
            counter += 1
        return h_expected
 
    def CompareTrigg(self,name):
       
        c = self.MakeCanvas2Pad(name)
        l = self.CreateLegend()
        
        p1 = c.GetPad(1)
        p2 = c.GetPad(2)   
        
        #Cogemos los histogramas de la muestra de ttbar
        s = self.GetSampleName("ttbar")           
        #With trigger
        h = s.GetHisto(name + '_forTrigg')
        #No trigger
        h2 = s.GetHisto(name + '_noTrigg')
        
        p1.cd()
        h.GetXaxis().SetLabelSize(0.0)
        h.SetMaximum(h2.GetMaximum() * 1.4)
        h.SetFillColor(0)
        h.SetLineColor(r.kBlue)
        h2.SetFillColor(0)
        h2.SetLineColor(r.kRed)
        h.Draw("HIST")
        h2.Draw("HIST SAME")
             
        self.AddEntry(h, l, "Pasa #font[12]{Trigger}", "f")
        self.AddEntry(h2, l, "No pasa #font[12]{Trigger}", "f")
     
        if self.title  != '': 
            h.SetTitle("") 
        
        if self.ytitle != '': 
            h.GetYaxis().SetTitle(self.ytitle)     
        #Ratio
        Ratio = deepcopy(h.Clone("Ratio"))
        Ratio.Divide(h2)
        Ratio.SetFillColor(r.kCyan - 10)
        Ratio.SetLineColor(r.kBlack)
        l.Draw("SAME")
        
        p2.cd()
        Ratio.Draw("HIST")
        if name == 'MuonPt':
            bbox1 = self.CreateCommentBox(24, 0, 30, 1, r.kBlue)
            self.Annotate(0.45, 0.92, "Eff: %3.2f"%(h.Integral(8, 20)/h2.Integral(8, 20)))
            bbox2 = self.CreateCommentBox(25, 0, 30, 0.9,r.kRed)
            self.Annotate(0.5, 0.7, "Eff: %3.2f"%(h.Integral(10, 20)/h2.Integral(10, 20)))
            bbox3 = self.CreateCommentBox(26, 0, 30, 0.6, r.kGreen)
            self.Annotate(0.6, 0.5, "Eff: %3.2f"%(h.Integral(12, 20)/h2.Integral(12, 20)))
            bbox1.Draw("SAME")
            bbox2.Draw("SAME")
            bbox3.Draw("SAME")
        
        if self.xtitle != '':
            Ratio.SetMaximum(1.0)
            Ratio.GetXaxis().SetTitle()
            Ratio.GetXaxis().SetTitleSize(0.07)
            Ratio.GetXaxis().SetLabelSize(0.03)
        
        Ratio.GetYaxis().SetTitle(r'\frac{Trigger}{NoTrigger}')
        Ratio.SetTitle('')
        Ratio.GetYaxis().SetTitleSize(0.06)
        Ratio.SetMaximum(Ratio.GetMaximum() * 1.2)
        p1.cd()
        for note in self.Annotations:
            self.Annotate(float(note[2]), float(note[3]), note[1])
            
        F.create_folder(self.savepath)
        c.Print(self.savepath + "/" + name + 'TriggComp' + '.png', 'png')
        c.Print(self.savepath + "/" + name + 'TriggComp' + '.pdf', 'pdf')
        c.Close()
        return       
       
    def Stack(self, name):
        ''' Produce a stack plot for a variable given '''
        if (isinstance(name, list)):
            for nam in name: self.Stack(nam)
            return
        
        c = self.MakeCanvas2Pad(name)
        l = self.CreateLegend()
        p1 = c.GetPad(1)
        p2 = c.GetPad(2)
        
        hstack = self.GetStackedHistos(name)
        self.AddEntry(hstack.GetHists(), l, name = self.listOfSelectors)
        
        h_expected = self.GetExpectedHist(name)
        self.AddEntry(h_expected, l, name = "stat.Unc" )
        
        #Draw stacked plot in PAD1:
        p1.cd()
        hstack.Draw("hist")
        hstack.GetXaxis().SetLabelSize(0.0)
        h_expected.Draw("E2 same")
        
        if self.LogY        : p1.SetLogy()       
        if self.title  != '': hstack.SetTitle("")
        if self.ytitle != '': hstack.GetYaxis().SetTitle(self.ytitle)
        #hstack.GetYaxis().SetTitleOffset(1.35)
        Max = hstack.GetStack().Last().GetMaximum();    


        if self.data != '':
            hdata = self.dataSelector.GetHisto(name)
            hdata.SetMarkerStyle(20)
            hdata.SetMarkerColor(1)
            hdata.Draw("pe1same")
            MaxData = hdata.GetMaximum()
            if(Max < MaxData): Max = MaxData
            self.AddEntry(hdata, l, "data", "p")

            #Get data/expected if data given
            h_ratio = F.GetRatioHist(hdata, h_expected,name ,self.xtitle)
            h_ratio.SetMarkerStyle(20)
            p2.cd()           
            h_ratio.Draw("pe1same")
            p1.cd()
            
        hstack.SetMaximum(Max * 1.1)             
        l.Draw("same")
        
        for note in self.Annotations:
            self.Annotate(float(note[2]), float(note[3]), note[1])
    
        F.create_folder(self.savepath)
        c.Print(self.savepath + "/" + name + '.png', 'png')
        c.Print(self.savepath + "/" + name + '.pdf', 'pdf')
        c.Close()
        return

    def PrintCounts(self, name):
        ''' Print the number of events for each sample in a given histogram '''
        if (isinstance(name, list)):
            for nam in name: self.PrintEvents(nam)
            return

        print "\nPrinting number of events for histogram {h}:".format(h = name)
        print '----------------------------------------------------'
        total = 0.
        for s in self.listOfSelectors:
            h = s.GetHisto(name)
            print "{nam}: {num}".format(nam = s.name, num = h.Integral())
            total += h.Integral()

        print 'Expected (MC): {tot}'.format(tot = total)
        print '------------------------------'
        if self.data != '':
            hdata = self.dataSelector.GetHisto(name)
            print 'Observed (data): {tot}'.format(tot = hdata.Integral())
            print '------------------------------'
        return


    def SaveCounts(self, name, overridename = ""):
        ''' Save in a text file the number of events for each sample in a given histogram '''
        if (isinstance(name, list)):
            for nam in name: self.SaveCounts(nam, overridename = overridename)
            return

        filename = "yields_{h}".format(h = name) if (overridename == "") else overridename
        F.create_folder(self.savepath)
        outfile = open(self.savepath + "/" + filename + (".txt" if ".txt" not in overridename else ""), "w")

        thelines = []

        thelines.append("Number of events for histogram {h}:\n".format(h = name))
        thelines.append("----------------------------------------------------\n")
        #total = 0.
        for s in self.listOfSelectors:
            h = s.GetHisto(name)
            thelines.append("{nam}: {num}\n".format(nam = s.name, num = h.Integral()))
            #total += h.Integral()
        
        thelines.append('Expected (MC): {tot}\n'.format(tot = self.GetExpectedEvents(name)))
        thelines.append('------------------------------\n')
        if self.data != '':
            hdata = self.dataSelector.GetHisto(name)
            thelines.append('Observed (data): {tot}\n'.format(tot = hdata.Integral()))
            thelines.append('------------------------------\n')

        outfile.writelines(thelines)
        outfile.close()
        return
    
    def DrawHistos(self):
        print(self.savepath)
        for histo in self.Histos:
            #Spaces in labels must be delimited by  "-" 
            self.SetXtitle(histo[1].replace("|", " "))
            self.SetYtitle(histo[2].replace("|", " "))
            self.SetTitle(histo[3].replace("|", " "))
            if histo[4] == '1': self.SetLogScale() #if 1, change the scale of the pad
            self.Stack(histo[0])
            if (histo[0] == 'MuonPt'): self.CompareTrigg(histo[0])
            #self.SaveCounts(histo[0])



