import codecs
import pandas as pd
import numpy as np

class ConverterBase(object):

    """
    A base class for generating processed datasets.
    """

    def __init__(self):
        self.col  = None
        self.col_to_use = None

    def getData(self, filepath):
        with codecs.open(filepath, "r", "Shift-JIS", "ignore") as file:
            df = pd.read_table(file, delimiter=",")

        df = df.ix[8:, :len(self.col)]
        df.columns = self.col
        df = df[self.col_to_use]

        df = df.replace('＊', np.nan)
        df = df.replace('−', np.nan)
        df = df[df.Label != '景気の現状判断']
        df = df.dropna()
        df.Comment = list(self.getComment(df.Comment))

        return df

    def getComment(self, comment):
        for c in comment:
            yield c[1:]

class ConverterGenjou(ConverterBase):
    """
    A class for Genjou
    """

    def __init__(self):
        ConverterBase.__init__(self)
        self.col = ['Fields', 'TokyoFlag', 'Label', 'Job', 'Reason', 'Comment']
        self.col_to_use = ['Label', 'Job', 'Reason', 'Comment']

class ConverterSakiyuki(ConverterBase):
    """
    A class for Sakiyuki
    """

    def __init__(self):
        ConverterBase.__init__(self)
        self.col = ['Fields', 'TokyoFlag', 'Label', 'Job', 'Comment']
        self.col_to_use = ['Label', 'Job', 'Comment']

if __name__ == '__main__':
    cg = ConverterGenjou('watcher4.csv')
    print(cg.getData())

    cs = ConverterSakiyuki('watcher5.csv')
    print(cs.getData())
