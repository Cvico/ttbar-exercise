
class Histos:
    ''' Class to store information about the histograms that are going
    to be created'''
    name   = "foo"
    x_axis = []
    xlabel = "xlabel"
    ylabel = "ylabel"
    logy   = 0
    def __init__(self, info):
        self.name   = info[0]
        self.x_axis = info[1]
        self.xlabel      = info[2]
        self.ylabel      = info[3]
        self.logy        = info[4]
        return

