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
    return parser


if __name__ == "__main__":
    # Create a parser where to specify actions
    parser = add_Parsing_options()
    an = FAEA_Analysis('./plots.txt', 'data')


