import numpy as np
import pandas as pd
import sqlite3

from Converter import ConverterGenjou, ConverterSakiyuki
from urllib import request

"""
調査の公表日を指定して当該月のデータのみを取得してデータベースへ追加するスクリプト。
事前にScraping.pyとDataBase.pyを実行し、同じディレクトリにdata.dbとdata.csvを生成しておく必要がある。
"""

def main(date):
    # 日付からダウンロードするcsvファイルのurlを生成
    url4 = 'http://www5.cao.go.jp/keizai3/' + date[:4] + '/' + date[4:] + 'watcher/watcher4.csv'
    url5 = 'http://www5.cao.go.jp/keizai3/' + date[:4] + '/' + date[4:] + 'watcher/watcher5.csv'

    # 生成したurlを表示
    print(url4)
    print(url5)

    # 生成したurlからcsvファイルをダウンロードし、CSVFilesフォルダ以下に保存。
    path4 = 'CSVFiles/' + date + 'watcher4.csv'
    path5 = 'CSVFiles/' + date + 'watcher5.csv'
    request.urlretrieve(url4, path4)
    request.urlretrieve(url5, path5)

    #　先行きと現状のcsvファイル変換用のインスタンスを生成
    cg = ConverterGenjou()
    cs = ConverterSakiyuki()

    # 保存したcsvファイルを読み込み、DataFrame形式に変換
    df4 = cg.getData(path4) # 現状データの読み込み
    df4['type'] = '現状'
    df4['year'] = date[:4]
    df4['month'] = date[4:6]

    df5 = cs.getData(path5) # 先行きデータの読み込み
    df5['type'] = '先行き'
    df5['Reason'] = np.nan
    df5['year'] = date[:4]
    df5['month'] = date[4:6]

    # データベースへ保存
    conn = sqlite3.connect("data.db")
    df4.to_sql('data', conn, index=False, if_exists='append')
    df5.to_sql('data', conn, index=False, if_exists='append')

    # data.csvをアップデート
    df_sql = pd.read_sql('select * from data', conn)
    df_sql.to_csv('data.csv', encoding="Shift-JIS", index=False)

if __name__ == '__main__':
    date = '20171109' # 公表日をyyyymmddの形式で指定（例:平成29年11月9日公表=20171109）
    main(date)
