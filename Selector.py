# -*- coding: utf-8 -*-
import os
import warnings as wr
import ROOT as r
import Functions as F

class Selector:
    ''' Class to do an event selection'''
    ### =============================================
    ### Constructor
    def __init__(self, filename = '', hist_list, savepath = ""):
        ''' Initialize a new Selector by giving the name of a sample.root file '''
        self.name = filename
        self.hist_list = hist_list
        self.filename = self.name
        self.savepath = savepath
        if self.filename[-5:] != '.root': self.filename += '.root'
        if not os.path.exists(self.filename): self.filename = '../files/' + self.filename
        if not os.path.exists(self.filename):
            if (self.name != ''): wr.warn("[Selector::constructor] WARNING: file {f} not found".format(f = self.name))
        else:
            self.CreateHistograms()
            print(self.histograms)
            #self.SetSystematic()
            #self.ApplySelectionCut()
            #self.Loop()
            #if self.GetSampleName() == "ttbar": self.Loop_gen()
            #self.WriteHistograms()
            #self.WriteLog()
        return

    ### =============================================
    ### Attributes
    # General
    histograms = []
    name = ""
    filename = ""
    savepath = ""
    OutfileName = ""
    syst = 1 # Incertidumbre sistematica de la muestra

    
    # Histogram variables
    muon1_pt = -99
    invmass = -99
    weight = -99
    muon1_eta = -99
    Njets_B = -99
    Njets_B_good = -99
    bJet_pt = 0 
    
    # Cut Variables
    # == Trigger
    triggerIsoMu24 = False
    # == Variables para muones
    Nmuon = 0
    Muon_Pt = -99
    Muon_Eta = -99
    # == Variables para jets
    NJet = 0
    Jet_Pt = -99
    Jet_Eta = -99
    # == Corte para b-jets
    NbJets = 0
    bTags_WP = 3.0 #Working point for bTags
    event_DR = -99
    # == Variable para MET
    event_MET = -99
    
    ### =============================================
    ### Methods
    def SetSystematic(self):
        ''' Este metodo establece la incertidumbre sistematica 
            que se asume para una muestra dada'''
        Info = F.LoadTxtFile('systematics.txt')
        for line in Info:
            if line[0] == self.name: self.syst = float(line[1])
            
    def GetSystematic(self):
        return self.syst
    
    def ApplySelectionCut(self):
        '''This method extracts the cut from the txt and set the variables for that cut'''
        Info = F.LoadTxtFile("cut.txt")
  
        for line in Info:
            # == Corte para muones
            if line[0] == 'Nmuon':
                self.Nmuon = int(line[1])
            if line[0] == 'Muon_Pt':
                self.Muon_Pt = float(line[1])
            if line[0] == 'Muon_Eta':
                self.Muon_Eta = float(line[1])
            # == Corte para jets
            if line[0] == 'NJet':
                self.NJet = int(line[1])
            if line[0] == 'Jet_Pt':
                self.Jet_Pt = int(line[1])
            if line[0] == 'Jet_Eta':
                self.Jet_Eta = float(line[1])
            # == Corte para b-jets
            if line[0] == 'NbJets':
                self.NbJets = int(line[1])
            if line[0] == 'bTags_WP':
                self.bTags_WP = float(line[1])
            if line[0] == 'DR':
                self.event_DR = float(line[1])
            # == Corte para MET    
            if line[0] == 'MET':
                self.event_MET = float(line[1])           
    def WriteHistograms(self):
        ''' Escribimos los histogramas en una rootfile para no
            tener que leer las muestras una y otra vez     '''
        name = "histos"
        #OutFileName = name + "_" + self.GetSampleName() + ".root"
        OutFileName = name + ".root"
        OutFilePath = self.savepath + "/rootfiles/"  

        if not os.path.exists(OutFilePath):
            print("[INFO]Creando PATH %s para guardar los histogramas..."%OutFilePath)
            F.create_folder(OutFilePath)
        
        if not os.path.exists(OutFilePath + OutFileName):
            OutFile = r.TFile.Open(OutFilePath + "/" + OutFileName, "recreate")
        
        else:
            OutFile = r.TFile.Open(OutFilePath + "/" + OutFileName, "UPDATE")
        #if os.path.exists(outfilepath + outfilename): 
            #print("[info] el fichero %s ya existe en el directorio %s"%(outfilename, self.savepath))
            #print("[info] creando backup...")
            #outfilename = outfilename[:-6] + "_bck.root" 
            

        
        print("[INFO] El fichero  %s ha sido creado correctamente"%(OutFileName))
        print("[INFO] Escribiendo histogramas dentro de la rootfile...")
        sample = self.GetSampleName()
        self.GetHisto('MuonPt').Write('MuonPt_%s'%sample)
        self.GetHisto('MuonPt_Gen').Write('MuonPt_Gen%s'%sample)
        self.GetHisto('Njet').Write('Njet_%s'%sample)
        self.GetHisto('MET').Write('MET_%s'%sample)
        self.GetHisto('MET_Gen').Write('MET_Gen%s'%sample)
        self.GetHisto('MuonPt_noTrigg').Write('MuonPt_noTrigg%s'%sample)
        self.GetHisto('MuonPt_forTrigg').Write('MuonPt_forTrigg_%s'%sample)
        self.GetHisto('MuonEta').Write('MuonEta_%s'%sample)
        self.GetHisto('MuonEta_noTrigg').Write('MuonEta_noTrigg_%s'%sample)
        self.GetHisto('MuonEta_forTrigg').Write('MuonEta_forTrigg_%s'%sample)
        self.GetHisto('NbJets').Write('NbJets_%s'%sample)
        self.GetHisto('NandBjetsCompare').Write('NandBjetsCompare_%s'%sample)
        self.GetHisto('WeightsGen').Write('WeightsGen_%s'%sample)

        OutFile.Close()    
    
    def WriteLog(self):
        filename = "cut_applied" 
        F.create_folder(self.savepath)
        outfile = open(self.savepath + "/" + filename + ".txt", "w")
        
        thelines = []
        thelines.append("Cut applied for this run \n")
        thelines.append("---------------------------\n")
        thelines.append("Trigg: " + str(self.triggerIsoMu24) + "\n")
        thelines.append("Nmuon: " + str(self.Nmuon) + "\n")
        thelines.append("NbJets: " + str(self.NbJets) + "\n")
        thelines.append("bTags_WP: " + str(self.bTags_WP) + "\n")
        thelines.append("NJet: " + str(self.NJet) + "\n")
        thelines.append("Muon1Pt: " + str(self.Pt_muon1) + "\n")
        thelines.append("Muon2Pt: " + str(self.Pt_muon2) + "\n")
        thelines.append("MET: " + str(self.event_MET) + "\n")
        thelines.append("Eta: " + str(self.event_Eta) + "\n")
        outfile.writelines(thelines)
        outfile.close()

    def GetSampleName(self):
        return self.name
    def create_histograms(self):
        for hist in self.hist_list:
            self.histograms.append(r.TH1F(self.name + hist.name, ";".join(hist.xlabel, hist.ylabel), hist.x_axis[0], hist.x_axis[1], hist.x_axis[2]))
        return
    def CreateHistograms(self):
        ''' CREATE YOUR HISTOGRAMS HERE '''
        self.histograms = []
        self.histograms.append(r.TH1F(self.name + '_MuonPt',     ';p_{T}^{#mu} (GeV);Events', 20, 0, 200))
        self.histograms.append(r.TH1F(self.name + '_MuonPt_Gen',     ';p_{T}^{#mu} (GeV);Events', 20, 0, 200))       
        #self.histograms.append(r.TH1F(self.name + '_DiMuonMass', ';m^{#mu#mu} (GeV);Events',  20, 0, 200))
        self.histograms.append(r.TH1F(self.name + '_Njet', ';Njets; Events',10, 0, 10))
        self.histograms.append(r.TH1F(self.name + '_MET', ';MET;Events', 30,0,200))
        self.histograms.append(r.TH1F(self.name + '_MET_Gen', ';MET;Events0', 30, 0, 200))
        self.histograms.append(r.TH1F(self.name + '_MuonPt_noTrigg', ';P_{T}^{#MU} (GeV);Events', 20, 20, 30))
        self.histograms.append(r.TH1F(self.name + '_MuonPt_forTrigg', ';P_{T}^{#MU} (GeV);Events', 20, 20, 30))
        self.histograms.append(r.TH1F(self.name + '_MuonEta', ';#ETA;Events',20 ,-3, 3))
        self.histograms.append(r.TH1F(self.name + '_MuonEta_noTrigg', ';#ETA;Events',20 ,-3, 3))
        self.histograms.append(r.TH1F(self.name + '_MuonEta_forTrigg', ';#ETA;Events',20 ,-3, 3))
        self.histograms.append(r.TH1F(self.name + '_NbJets', ';NbJets;Events', 5, 0, 5))
        self.histograms.append(r.TH1F(self.name + '_NbJets_gen_den', ';NbJets_den;Events', 5, 0, 5))
        self.histograms.append(r.TH1F(self.name + '_NbJets_gen_num', ';NbJets_gen;Events', 5, 0, 5))
        self.histograms.append(r.TH1F(self.name + '_NandBjetsCompare', ';xlabel;Events', 7, 0, 6))
        self.histograms.append(r.TH1F(self.name + '_WeightsGen', ';xlabel;Events', 100, 0, 1))
        return

    def GetHisto(self, name):
        ''' Use this method to access to any stored histogram '''
        for h in self.histograms:
            n = h.GetName()
            if self.name + '_' + name == n: return h
        wr.warn("[Selector::GetHisto] WARNING: histogram {h} not found.".format(h = name))
        return r.TH1F()


    def FillHistograms(self):
        self.GetHisto('MuonPt').Fill(self.muon_pt,    self.weight)
        #self.GetHisto('DiMuonMass').Fill(self.invmass, self.weight)
        self.GetHisto('Njet').Fill(self.NJetsReco, self.weight)
        self.GetHisto('MET').Fill(self.MET, self.weight)   
        self.GetHisto('MuonEta').Fill(self.muon_eta, self.weight)
        self.GetHisto('NbJets').Fill(self.Njets_B, self.weight)
        self.GetHisto('NbJets_gen_num').Fill(self.Njets_B_good, self.weight)
        self.GetHisto('NbJets_gen_den').Fill(2, self.weight)
        return

    def FillHistogramsGen(self):
        self.GetHisto('MuonPt_Gen').Fill(self.MCmuon_pt, self.weight)
        return
    
    def FillHistogramsWeights(self, weight):
        self.GetHisto('WeightsGen').Fill(weight, weight)
        return
    
    def FillHistogramsNoTrigg(self):
        self.GetHisto('MuonPt_noTrigg').Fill(self.muon_pt, self.weight)
        self.GetHisto('MuonEta_noTrigg').Fill(self.muon_eta, self.weight)
        return
    
    def FillHistogramsForTrigg(self):
        self.GetHisto('MuonPt_forTrigg').Fill(self.muon_pt, self.weight)       
        self.GetHisto('MuonEta_forTrigg').Fill(self.muon_eta, self.weight)
        return 
    
    def FillNandBJetComparison(self):
        if (self.Njets_B == 0 and self.NJetsReco == 1):
            self.GetHisto('NandBjetsCompare').Fill(0, self.weight)
        if (self.Njets_B == 1 and self.NJetsReco == 1):
            self.GetHisto('NandBjetsCompare').Fill(1, self.weight)
        if (self.Njets_B == 0 and self.NJetsReco == 2):
            self.GetHisto('NandBjetsCompare').Fill(2, self.weight)
        if (self.Njets_B == 1 and self.NJetsReco == 2):
            self.GetHisto('NandBjetsCompare').Fill(3, self.weight)
        if (self.Njets_B == 0 and self.NJetsReco == 3):
            self.GetHisto('NandBjetsCompare').Fill(4, self.weight)
        if (self.Njets_B == 1 and self.NJetsReco == 3):
            self.GetHisto('NandBjetsCompare').Fill(5, self.weight)
        if (self.Njets_B == 0 and self.NJetsReco == 4):
            self.GetHisto('NandBjetsCompare').Fill(6, self.weight)
        return
        
    def Loop_gen(self):
        print("making analysis")
        f = r.TFile.Open(self.filename)
        tree = f.events
        nEvents = tree.GetEntries()
        print("Opening file {f} and looping over {n} events...".format(f = self.filename, n = nEvents))
        for event in tree:

            if abs(event.MCleptonPDGid) != 13: continue
            MCmuon = r.TLorentzVector()
            
            MCmuon.SetPx(event.MClepton_px)
            MCmuon.SetPy(event.MClepton_py) 
            MCmuon.SetPz(event.MClepton_pz)

            
            self.MCmuon_pt = MCmuon.Pt()
            self.MCmuon_eta = MCmuon.Eta()
            self.MC_MET = (event.MCneutrino_px*event.MCneutrino_px + event.MCneutrino_py*event.MCneutrino_py)**(0.5)
            
            if self.MCmuon_pt < self.Muon_Pt: continue
            if abs(self.MCmuon_eta) > self.Muon_Eta: continue
            if self.MC_MET < self.event_MET: continue

        
            self.weight = event.EventWeight
            self.FillHistogramsGen()      
    
    def Loop_new(self):
        ''' Main method, used to loop over all the entries '''
        f = r.TFile.Open(self.filename)
        tree = f.events
        nEvents = tree.GetEntries()
        print
        "Opening file {f} and looping over {n} events...".format(f=self.filename, n=nEvents)

        for event in tree:
            string = ""
            # Rellenamos el histograma de pesos, pesando cada uno de ellos por si mismo
            # de esta manera obtenemos la cantidad de sucesos generados pesada a nuestra
            # luminosidad

            self.FillHistogramsWeights(event.EventWeight)

            ### Pedimos 1 muon
            if event.NMuon < self.Nmuon: continue

            ### Definimos un muon a partir de su 4-momento
            muon = r.TLorentzVector()
            muon.SetPxPyPzE(event.Muon_Px[0], event.Muon_Py[0], event.Muon_Pz[0], event.Muon_E[0])

            # Si la muestra analizada es ttbar entonces la utilizamos para calcular la eficiencia
            # de trigger

            if self.GetSampleName() == "ttbar":  #
                # Calculamos las propiedades del muon antes de pasar el trigger
                self.weight = event.EventWeight
                self.muon_pt = muon.Pt()
                self.muon_eta = muon.Eta()
                self.FillHistogramsNoTrigg()

            # Si no pasa el trigger no lo registramos para el analisis
            if not event.triggerIsoMu24: continue

            # Calculamos las propiedades del muon despues de pasar el trigger
            self.muon_pt = muon.Pt()
            self.muon_eta = muon.Eta()
            # self.Njet = event.NJet
            self.MET = (event.MET_px * event.MET_px + event.MET_py * event.MET_py) ** (0.5)

            # solamente para la muestra de ttbar
            if self.GetSampleName() == "ttbar":
                self.weight = event.EventWeight
                self.FillHistogramsForTrigg()

                # corte de variables cinemáticas
            if self.muon_pt < self.Muon_Pt: continue
            if self.MET < self.event_MET: continue
            if abs(self.muon_eta) > self.Muon_Eta: continue
            # corte en jets y bjets
            RecoJets = self.ObtainJetInfo(event)
            if self.NJetsReco < self.NJet: continue
            bJets_reco = self.CheckForBtags(event)
            if self.Njets_B < self.NbJets: continue
            if self.GetSampleName() == 'ttbar': self.B_taggEff(event, bJets_reco)

            # aplicamos el peso en función de la cantidad de bJets que pidamos
            peso_bJets = 1
            if self.Njets_B >= 2:
                peso_bJets = (0.86)
            elif self.Njets_B == 1:
                peso_bJets = 0.9

                # aplicamos el peso total del suceso
            self.weight = event.EventWeight * peso_bJets if not self.name == 'data' else 1

            # Rellenamos los histogramas
            self.FillNandBJetComparison()
            self.FillHistograms()

        return
    def Loop(self):
        ''' Main method, used to loop over all the entries '''
        f = r.TFile.Open(self.filename)
        tree = f.events
        nEvents = tree.GetEntries()
        print "Opening file {f} and looping over {n} events...".format(f = self.filename, n = nEvents)
        
        for event in tree:
            #Rellenamos el histograma de pesos, pesando cada uno de ellos por si mismo
            #de esta manera obtenemos la cantidad de sucesos generados pesada a nuestra
            #luminosidad
            
            self.FillHistogramsWeights(event.EventWeight) 
            
            ### Pedimos 1 muon
            if event.NMuon < self.Nmuon: continue       

            ### Definimos un muon a partir de su 4-momento
            muon = r.TLorentzVector()
            muon.SetPxPyPzE(event.Muon_Px[0], event.Muon_Py[0], event.Muon_Pz[0], event.Muon_E[0])
            
            #Si la muestra analizada es ttbar entonces la utilizamos para calcular la eficiencia
            #de trigger
            
            if self.GetSampleName() == "ttbar": #
                #Calculamos las propiedades del muon antes de pasar el trigger
                self.weight = event.EventWeight
                self.muon_pt = muon.Pt()
                self.muon_eta = muon.Eta()
                self.FillHistogramsNoTrigg()
                
            #Si no pasa el trigger no lo registramos para el analisis
            if not event.triggerIsoMu24: continue
            
            #Calculamos las propiedades del muon despues de pasar el trigger
            self.muon_pt = muon.Pt()
            self.muon_eta = muon.Eta()
            #self.Njet = event.NJet
            self.MET = (event.MET_px*event.MET_px + event.MET_py*event.MET_py)**(0.5)

            #solamente para la muestra de ttbar
            if self.GetSampleName() == "ttbar": 
                self.weight = event.EventWeight
                self.FillHistogramsForTrigg()           
            
            
            #corte de variables cinemáticas
            if self.muon_pt < self.Muon_Pt: continue
            if self.MET < self.event_MET: continue
            if abs(self.muon_eta) > self.Muon_Eta: continue 
            #corte en jets y bjets
            RecoJets = self.ObtainJetInfo(event)
            if self.NJetsReco < self.NJet: continue
            bJets_reco = self.CheckForBtags(event)
            if self.Njets_B < self.NbJets: continue 
            if self.GetSampleName() == 'ttbar': self.B_taggEff(event, bJets_reco)
          
            #aplicamos el peso en función de la cantidad de bJets que pidamos
            peso_bJets = 1
            if self.Njets_B  >= 2:
                peso_bJets = (0.86)
            elif self.Njets_B  == 1:
                peso_bJets = 0.9    
            
            #aplicamos el peso total del suceso
            self.weight = event.EventWeight * peso_bJets if not self.name == 'data' else 1
 
            #Rellenamos los histogramas
            self.FillNandBJetComparison()
            self.FillHistograms()     
 
        return
    def ObtainJetInfo(self, event):
        ''' Este metodo se utiliza para obtener la información correspondiente a un jet '''
        nJets = event.NJet 
        RecoJets = [] # Jets que pasan los cortes establecidos
        for jet in range(nJets):
            ''' Informacion disponible del jet '''
            Jet = r.TLorentzVector()
            Jet.SetPxPyPzE(event.Jet_Px[jet], event.Jet_Py[jet], event.Jet_Pz[jet], event.Jet_E[jet])
            Jet_Pt = Jet.Pt()
            Jet_Eta = Jet.Eta()
            
            if Jet_Pt < self.Jet_Pt: continue
            if abs(Jet_Eta) > self.Jet_Eta: continue
        
            RecoJets.append([Jet_Pt, Jet_Eta])
        self.NJetsReco = len(RecoJets)    
        return RecoJets
        
    def CheckForBtags(self, event):
        ''' Use this method to measure the quality of a bJet and apply the cut to your analysis'''
        Jet_btag = event.Jet_btag
        N_jets_found = 0 #Number of jets we find
        bJets_reco = []
        counter = -1
        for b_Jet in Jet_btag:
            counter += 1
            if b_Jet == -1: continue 
            if b_Jet < self.bTags_WP: continue
            #Jet de reconstruccion
            bJet = r.TLorentzVector()
            bJet.SetPxPyPzE(event.Jet_Px[counter], event.Jet_Py[counter], event.Jet_Pz[counter], event.Jet_E[counter])
            
            bJet_Pt = bJet.Pt()
            bJet_eta = bJet.Eta()
            bJet_phi = bJet.Phi()
            if abs(bJet_eta) > self.Jet_Eta: continue
            if bJet_Pt < self.Jet_Pt: continue
            bJet_info = [bJet_Pt, bJet_eta, bJet_phi]
            N_jets_found += 1 
            bJets_reco.append(bJet_info)
            
        self.Njets_B = N_jets_found
        return bJets_reco
    
    def B_taggEff(self, event, bJets):
        ''' Bjets es una lista con info sobre los jets de reco'''
        # bjets[njet] = [Pt, eta, phi]
        N_bJets_good = 0
        # Calculamos la eficiencia de b_tagging
        # bTags de generacion
        WbottomQ = r.TLorentzVector()
        WbottomQ.SetPx(event.MChadronicWDecayQuark_px)
        WbottomQ.SetPy(event.MChadronicWDecayQuark_py)           
        WbottomQ.SetPz(event.MChadronicWDecayQuark_pz)            
        WbottomQ_Eta = WbottomQ.Eta()
        WbottomQ_Phi = WbottomQ.Phi()
        
        WbottomQbar = r.TLorentzVector()
        WbottomQbar.SetPx(event.MChadronicWDecayQuarkBar_px)
        WbottomQbar.SetPy(event.MChadronicWDecayQuarkBar_py)           
        WbottomQbar.SetPz(event.MChadronicWDecayQuarkBar_pz)            
        WbottomQbar_Eta = WbottomQbar.Eta()
        WbottomQbar_Phi = WbottomQbar.Phi()
                
        bottomQ = r.TLorentzVector()
        bottomQ.SetPx(event.MChadronicBottom_px)
        bottomQ.SetPy(event.MChadronicBottom_py)           
        bottomQ.SetPz(event.MChadronicBottom_pz)            
        bottomQ_Eta = bottomQ.Eta()
        bottomQ_Phi = bottomQ.Phi()
            
        lepBottomQ = r.TLorentzVector()
        lepBottomQ.SetPx(event.MCleptonicBottom_px)
        lepBottomQ.SetPy(event.MCleptonicBottom_py)           
        lepBottomQ.SetPz(event.MCleptonicBottom_pz)            
        lepBottomQ_Eta = lepBottomQ.Eta()
        lepBottomQ_Phi = lepBottomQ.Phi()
        
        for bjet in bJets:
            bJet_Eta = bjet[1]
            #print(bJet_eta)
            bJet_Phi = bjet[2]
            DR1 = ((bJet_Eta - WbottomQ_Eta)**2 + (bJet_Phi - WbottomQ_Phi)**2)**(0.5)
            DR2 = ((bJet_Eta - WbottomQbar_Eta)**2 + (bJet_Phi - WbottomQbar_Phi)**2 )**(0.5)
            DR3 = ((bJet_Eta - bottomQ_Eta)**2 + (bJet_Phi - bottomQ_Phi)**2)**(0.5)
            DR4 = ((bJet_Eta - lepBottomQ_Eta)**2 + (bJet_Phi - lepBottomQ_Phi)**2)**(0.5)           
            #if DR1 < self.event_DR or DR2 < self.event_DR or DR3 < self.event_DR or DR4 < self.event_DR:
                #N_bJets_good += 1.0
            if DR1 < self.event_DR: N_bJets_good += 1
            elif DR2 < self.event_DR: N_bJets_good += 1
            elif DR3 < self.event_DR: N_bJets_good += 1
            elif DR4 < self.event_DR: N_bJets_good += 1
        #print('De {jets} jets, {bjets} son correctamente etiquetables'.format(jets = len(bJets), bjets = N_bJets_good))
        self.Njets_B_good = N_bJets_good
        return
               
               


                
                
               

