from Selector import Selector
from Plotter import Plotter
import numpy as np
from copy import deepcopy
import Functions as F
import ROOT as r
from test import FAEA_Analysis
import argparse
import pandas as pd


def add_parsing_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--Path', '-P', metavar="path", dest="path", default="../", help = "Path where the ntuples are stored")
    parser.add_argument('--mca', '-m', metavar = "mca_file", dest = "mca_file", default = "./info.txt", help = "Configuration for each sample")
    parser.add_argument('--plotfile', '-p', metavar = "plot_file", dest = "plot_file", default "./tt_plots.txt", help = "Plots that can be printed")
    return parser


if __name__ == "__main__":
    # Create a parser where to specify actions
    parser = add_Parsing_options()

    options = parser.parse_args()
    path = options.path
    mca_file = options.mca_file
    plot_file = options.plot_file
    # Run plotter
    Plotter()


