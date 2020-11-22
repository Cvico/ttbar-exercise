from Selector import Selector
from Plotter import Plotter
import numpy as np
from histos import Histos
import re
import ROOT as r
import argparse

r.gROOT.SetBatch(1) # To work only by batch (i.e. through terminal, w/o windows)
r.gStyle.SetOptStat(0)

def add_parsing_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path', '-P', metavar="path", dest="path", default="../", help = "Path where the ntuples are stored")
    parser.add_argument('--mca', '-m', metavar = "mca_file", dest = "mca_file", default = "./info.txt", help = "Configuration for each sample")
    parser.add_argument('--plotfile', '-p', metavar = "plot_file", dest = "plot_file", default = "./tt_plots.txt", help = "Plots that can be printed")
    parser.add_argument('--outpath', '-o', metavar = "outpath", dest = "outpath", default = "./Plots/", help = "outpath for results")
    return parser

def read_mca(mca_file):
    ''' This method is used to set up the list of backgrounds
        used for the analysis. It is mean to read a file which
        contains, in each line, the following structure:
            LABEL: ntuple_name : color

        It returns two dictionaries: one with the filenames
        and the other one with the colors that they should appear with
        in the plots.
    '''
    lines = open(mca_file, "r").readlines()
    list_of_selectors = {}
    colors = {}
    for line in lines:
        if line[0] == "#": continue # comment line
        line = re.sub(r"\s+", "", line).split(":") #remove spaces and split between regexp ":"
        list_of_selectors[line[0]] = line[1]
        colors[line[0]] = line[2] if (line[0] != "data") else "isData"
    return (list_of_selectors, colors)

def read_plot_file(plot_file):
    lines = open(plot_file, "r".readlines())
    histo_list = []
    for line in lines:
        if line[0] == "#": continue
        histo_list.append(Histos(re.sub(r"\s+", "", line).replace(";",":").split(":")))

    return histo_list
if __name__ == "__main__":
    # Create a parser where to specify actions
    parser = add_parsing_options()

    options = parser.parse_args()
    path = options.path
    mca_file = options.mca_file
    plot_file = options.plot_file

    # Read the mca files
    processes, colors = read_mca(mca_file)
    hist_list = read_plot_file(plot_file)
    print(processes)
    print(hist_list)
    # Run plotter


