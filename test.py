from Selector import Selector
from Plotter import Plotter
import numpy as np
from copy import deepcopy
import Functions as F
import ROOT as r
import os
r.gROOT.SetBatch(1) # To work only by batch (i.e. through terminal, w/o windows)
r.gStyle.SetOptStat(0)


class FAEA_Analysis:
    ''' Clase para correr los selectors y llamar a plotter'''
    ### ==================================================
    ### Constructor
    def __init__(self, infoRun, data = ''):
        self.infoRun = infoRun
        self.SetEnvironment(self.infoRun)
        self.data = data
        counter = 0
        
        # Imponemos los criterios de seleccion
        for bck in self.backgrounds:
            self.listOfSelectors.append(Selector(bck, self.savepath))
            counter += 1
        if (self.data != ''): self.dataSelector = Selector(self.data, self.savepath)
        
        # == Dibujamos los histogramas
        # Le pasamos los selectors y una serie de parametros
        # a la clase Plotter para poder representar
        p = Plotter(self.listOfSelectors, self.dataSelector, self.Histos, self.colors)
        p.SetSavePath(self.savepath)
        p.SetAnnotations(self.Annotations)
        p.DrawHistos()
        
        # ===== Calculamos la seccion eficaz
        # == Establecemos como atributos los parametros
        #    que influyen en el calculo de la seccion eficaz
        self.SetParameters('MuonPt')
        
        # == Una vez establecidos los parametros calculamos
        #    la seccion eficaz y su incertidumbre (sistematica)
        self.PrintXsection('MuonPt')
        return
    
    
    ### =================================================
    ### Atributos
    
    # ========= Atributos de configuracion ======
    infoRun = ''
    data = ''
    savepath = ''
    dataSelector = Selector()
    listOfSelectors = []
    backgrounds = []
    bck_syst = []
    Histos = []
    Annotations = []
   
    ### ========== Parametros para el calculo de xsection ===
    A = 1
    BR = 0.09732
    b_tagEff = 1
    L = 50 #pb^-1
    trigger_eff = 1
    muon_eff = 0.99
    Nbckg = 0
    Ndata = 0
    Nttbar = 0
    xsection = 0
    
    ### =========== Variaciones sistematicas de los parametros
    sist_L = 0.1
    sist_triggerEff = 0 # Inicializado a 0, depende de la propia eficiencia
    sist_A = 0 # Inicializado a 0
    sist_bTag = 0 #Inicializado a 0
    
    ### =========== Listas donde guardaremos las variaciones
    #               sistematicas up, down y total
    systematics_up = []
    systematics_down = []
    systematics_total = []
    
    ### ============ Diccionario de colores disponibles
    #                para las representaciones de histogramas
    
    color_dict = {'white':0, 'black':1, 'red':2, 'lime':3,
    'blue':4, 'yellow':5, 'violet':6, 'cyan':7, 'green':8,
    'weirdblue':9, 'gray':17, 'ligtblue':38, 'teal':r.kTeal}   
    colors = []
    
    ### Metodos
    # ============ Metodos de configuracion
    def SetEnvironment(self, config):
        '''This method sets the environment of datapaths and outpaths'''
        Info = F.LoadTxtFile(self.infoRun) 
        for line in Info:
            if line[0] == 'Outpath': 
                self.savepath = line[1]
                continue
            if line[0] == 'Tex' or line[0] == 'tex' or line[0] == 'TEX': 
                line[1] = line[1].replace("|", " ") #Make "-" spaces
                self.Annotations.append(line) 
            elif line[0] == 'MCsamples':
                for bck in line[1:]: self.backgrounds.append(bck)
            
            elif line[0] == 'colors':
                for color in line[1:]: 
                    self.colors.append(self.color_dict[color.lower()])
            else: self.Histos.append(line) 
    
    def GetSampleName(self, name):
        for s in self.listOfSelectors:
            if s.GetSampleName() == name: 
                return s
    
    # =====   SETTERS Y GETTERS =============
    def SetBranchingRatio(self, BR):
        self.BR = BR
        return
    
    def GetBranchingRatio(self):
        return self.BR
    
    def SetLumi(self, L):
        self.L = L
    
    def GetLumi(self):
        return self.L
    
    def SetTriggerEff(self, trigger_eff):
        self.trigger_eff = trigger_eff
        return
    
    def GetTriggerEff(self):
        s = self.GetSampleName('ttbar')
        h_trigg = s.GetHisto('MuonPt_forTrigg')
        h_noTrigg = s.GetHisto('MuonPt_noTrigg')
        bin1 = h_trigg.FindBin(25)
        bin2 = h_trigg.FindBin(30)
        et = h_trigg.Integral(bin1, bin2)/h_noTrigg.Integral(bin1, bin2)
        self.sist_triggerEff = (1-et)/2
        print ('trigger eff: {et}'.format(et = et))
        #print ('INCERTIDUMBRE EN EFICIENCIA DE TRIGGER: {e}'.format(e = self.sist_triggerEff))
        return et
    
    def SetAcceptance(self, A):
        self.A = A
        return
    
    def GetAcceptance(self):
        s = self.GetSampleName("ttbar")
        hFiducial = s.GetHisto('MuonPt_Gen')
        hWeights = s.GetHisto('WeightsGen')
        A = hFiducial.Integral()/(hWeights.Integral())/self.BR
        self.sist_A = self.GetRatioUncertainty(hFiducial.Integral(), hWeights.Integral())
        #print('SISTEMATIC UNCERTAINTY IN ACCEPTANCE: {a}'.format(a = self.sist_A))
        return A
    
    def GetBtaggingEff(self):
        s = self.GetSampleName('ttbar')
        
        hDen = s.GetHisto('NbJets_gen_den')
        hNum = s.GetHisto('NbJets_gen_num')
        # Calculamos la eficiencia y almacenamos su incertidumbre en la variable asociada
        # a la incertidumbre de b-tagging (asumiendo fuentes estadisticas)
        
        e = hNum.Integral(1, 2)/hDen.Integral() * 0.9
        #print('INCERTIDUMBRE EN EFICIENCIA DE B-TAGGING: {e}'.format(e = self.sist_bTag))
        # Calculamos su incertidumbre sistematica
        self.sist_bTag = self.GetRatioUncertainty(hNum.Integral(1, 2), hDen.Integral())
        #print('SISTEMATICO DE B_TAGG UNCERTAINTY: {b}'.format(b = self.sist_bTag))
        #print('b tagging efficiency: {btagEff}'.format(btagEff = e))
        return e
    
    def SetBtaggingEff(self, b_tagEff):
        self.b_tagEff = b_tagEff
        return 
    
    def GetRatioUncertainty(self, num, den):
        stat_num = (num)**(0.5)
        stat_den = (den)**(0.5)
        
        unc = ( (stat_num/den)**2 + (num * stat_den/den**2)**2 )**(0.5) 
        return unc
    def GetNttbar(self, name):
        s = self.GetSampleName('ttbar')
        h = s.GetHisto(name)
        return h.Integral()
    
    def SetXsection(self, xsection):
        self.xsection = xsection
        return
    
    def GetXsection(self):
        ''' Calculo de la x-section'''
        xsection = (self.Ndata - self.Nbckg + self.Nttbar)/self.BR/self.L/self.trigger_eff/self.A/self.b_tagEff
        return xsection
    
    def SetNttbar(self, Nttbar):
        self.Nttbar = Nttbar
        return
    
    def SetNbckg(self, Nbckg):
        self.Nbckg = Nbckg
        return
    
    def GetNdata(self, name):
        hdata = self.dataSelector.GetHisto(name)
        return hdata.Integral()
    
    def SetNdata(self, Ndata):
        self.Ndata = Ndata
        return 
    
    def GetXsectionForSyst(self, A, trigger_eff, b_tagEff, BR, L, Nbckg, Ndata, Nttbar):
        ''' Calculo de la x-section'''
        xsection = (Ndata - Nbckg + Nttbar)/BR/L/trigger_eff/A/b_tagEff
        return xsection
    
    
    # ===== Metodos para el calculo de la seccion eficaz
    def SetParameters(self, name):
        # == Calculamos los parametros
        A = self.GetAcceptance()
        Br = self.GetBranchingRatio()
        L = self.GetLumi()
        b_tagEff = self.GetBtaggingEff()
        trigger_eff = self.GetTriggerEff()
        Nbckg = self.GetExpectedEvents(name)
        Nttbar = self.GetNttbar(name)
        Ndata = self.GetNdata(name)
        xsection = self.GetXsection()
        
        # == Establecemos los valores 
        self.SetAcceptance(A)
        #self.SetBranchingRatio(BR)
        self.SetLumi(L)
        self.SetBtaggingEff(b_tagEff)
        self.SetTriggerEff(trigger_eff)
        self.SetNbckg(Nbckg)
        self.SetNttbar(Nttbar)
        self.SetNdata(Ndata)
        self.SetXsection(xsection)
        
        # == Establecemos las variaciones sistematicas
        # para eficiencias y aceptancia, que dependen de los valores
        
        
        return 
        
    def PrintXsection(self, name):
       
        # === Calculamos el valor nominal de la xsection despues de los cortes
        xsection = self.GetXsection()
        self.SetXsection(xsection)
        
        # === Implementamos las variaciones sistematicas
        self.SetSystematics(name)
        
        ''' MC systematics ''' 
        total_up = 0
        total_down = 0
        total = 0
        for i in range(len(self.systematics_up)):
            total_up += self.systematics_up[i] * self.systematics_up[i]
            total_down += self.systematics_down[i] * self.systematics_down[i]
            total += self.systematics_total[i] * self.systematics_total[i]
       
        print('inc.sist up   : {num}'.format(num = np.sqrt(total_up  )/xsection))
        print('inc.sist down : {num}'.format(num = np.sqrt(total_down)/xsection))
        print('inc.sist total: {num}'.format(num = np.sqrt(total     )/xsection))

        print("cross section of: %3.4f"%(xsection))
    
    def SetSystematics(self, name):
        # ==== Calculamos las variaciones sistematicas de Lumi, btagging, trigger y aceptancia
        ''' Sistematico en Lumi'''
        lumi_xsection_up = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff, self.BR, self.L + self.L*self.sist_L, self.Nbckg, self.Ndata, self.Nttbar) - self.xsection
        lumi_xsection_down = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff, self.BR, self.L - self.L*self.sist_L, self.Nbckg, self.Ndata, self.Nttbar) - self.xsection
        
        ''' Sistematico de btag '''
        btag_xsection_up = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff + self.b_tagEff * self.sist_bTag, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar) - self.xsection
        btag_xsection_down = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff - self.b_tagEff * self.sist_bTag, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar)- self.xsection
        
        ''' Sistematico de eff '''
        eff_xsection_up = self.GetXsectionForSyst(self.A, self.trigger_eff + self.trigger_eff * self.sist_triggerEff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar)-self.xsection
        eff_xsection_down = self.GetXsectionForSyst(self.A, self.trigger_eff - self.trigger_eff * self.sist_triggerEff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar)-self.xsection
        
        ''' Sistematico de Aceptancia'''
        A_xsection_up = self.GetXsectionForSyst(self.A + self.A*self.sist_A, self.trigger_eff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar)-self.xsection
        A_xsection_down = self.GetXsectionForSyst(self.A - self.A*self.sist_A, self.trigger_eff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar)-self.xsection
        
        # ==== Metemos los sistematicos en un atributo especifico para almacenar los sistematicos del analisis
        self.systematics_up.append(lumi_xsection_up)
        self.systematics_up.append(btag_xsection_up)
        self.systematics_up.append(eff_xsection_up)
        self.systematics_up.append(A_xsection_up)
        
        self.systematics_down.append(lumi_xsection_down)
        self.systematics_down.append(btag_xsection_down)
        self.systematics_down.append(eff_xsection_down)
        self.systematics_down.append(A_xsection_down)
        
        self.systematics_total.append( (lumi_xsection_up + lumi_xsection_down)/2 )
        self.systematics_total.append( (btag_xsection_up + btag_xsection_down)/2 )
        self.systematics_total.append( (eff_xsection_up + eff_xsection_down)/2 )
        self.systematics_total.append( (A_xsection_up + A_xsection_down)/2 )
        # ==== Calculamos las variaciones sistematicas provenientes de los fondos de MC
        for s in self.listOfSelectors:
            if s.GetSampleName() == 'ttbar': continue # No tomamos inc. sist en ttbar
            var_up = self.GetMCsystematicsUp(name, s)
            var_down = self.GetMCsystematicsDown(name, s)
            var_tot = (var_up + var_down)/2
            
            self.systematics_up.append(var_up)
            self.systematics_down.append(var_down)
            self.systematics_total.append(var_tot)
                   
        return 
    
    def GetMCsystematicsUp(self, name, s):
        Nbckg_syst = self.ComputeSystematics(name, s, s.GetSystematic(), True)
        Nbckg_rest = self.GetExpectedEvents(name, s.GetSampleName(), True)
        variation = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar) - self.xsection
        return variation
    
    def GetMCsystematicsDown(self, name, s):
        Nbckg_syst = self.ComputeSystematics(name, s, s.GetSystematic(), False)
        Nbckg_rest = self.GetExpectedEvents(name, s.GetSampleName(), True)
        variation = self.GetXsectionForSyst(self.A, self.trigger_eff, self.b_tagEff, self.BR, self.L, self.Nbckg, self.Ndata, self.Nttbar) - self.xsection
        return variation
    
    def ComputeSystematics(self,name, s, syst, up):
        ''' Esta funcion devuelve la cantidad de sucesos de fondo
            teniendo en cuenta las incertidumbres sistematicas '''
        h = s.GetHisto(name)
        # == Hacemos una copia para evitar alterar los histogramas de resultados
        hsyst = deepcopy(h.Clone("hsyst"))
        nbins = hsyst.GetNbinsX()
        for i in range(nbins):
            if (up == True): hsyst.SetBinContent(i, h.GetBinContent(i) + h.GetBinContent(i)*syst)
            else:    hsyst.SetBinContent(i, h.GetBinContent(i) - h.GetBinContent(i)*syst)
        total = hsyst.Integral()
        del hsyst # para la siguiente iteracion
        return total
    
    
    def GetExpectedEvents(self, name, sname_toExclude = 'none', exclude = False):
        # Si exclude == True entonces sample no es considerada
        # para el calculo de los expected events
        total = 0
        for s in self.listOfSelectors:
            if s.GetSampleName() == sname_toExclude and exclude == True: continue
            h = s.GetHisto(name)
            total += h.Integral()
        return total   

an = FAEA_Analysis('./plots.txt', 'data')
#an.PrintXsection('MuonPt')
