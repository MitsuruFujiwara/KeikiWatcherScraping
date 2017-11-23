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
        # 変換するファイルを開く
        with codecs.open(filepath, "r", "Shift-JIS", "ignore") as file:
            df = pd.read_table(file, delimiter=",")

        # 不要な列を削除し、カラム名を指定
        df = df.ix[8:, :len(self.col)]
        df.columns = self.col
        df = df[self.col_to_use]

        # 不要な行を削除
        df = df.replace('＊', np.nan)
        df = df.replace('−', np.nan)
        df = df[df.Label != '景気の現状判断']
        df = df[df.Label != '景気の先行き判断']
        df = df.dropna()

        #  景気判断理由文頭の・を削除
        df.Comment = list(self.getComment(df.Comment))

        return df

    def getComment(self, comment):
        #  景気判断理由文頭の・を削除するための関数
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
    # test
    cg = ConverterGenjou('watcher4.csv')
    print(cg.getData())

    cs = ConverterSakiyuki('watcher5.csv')
    print(cs.getData())
