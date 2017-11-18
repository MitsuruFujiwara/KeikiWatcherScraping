import numpy as np
import os
import pandas as pd
import sqlite3

from Converter import ConverterGenjou, ConverterSakiyuki

"""
CSVFilesフォルダ以下のcsvファイルからsqlite3形式のデータベース(data.db)を作成するスクリプト
"""

def main():
    # CSVFilesフォルダ以下の全ファイル名のリストを取得
    filelist = os.listdir('CSVFiles')

    # 保存用のデータベースを生成
    conn = sqlite3.connect("data.db")

    #　先行きと現状のcsvファイル変換用のインスタンスを生成
    cg = ConverterGenjou()
    cs = ConverterSakiyuki()

    for f in filelist:

        # ファイルパスを指定
        path = 'CSVFiles/' + f
        print(path)

        # 年と月を取得
        y = f[:4]
        m = int(f[4:6])

        # 現状or先行きのデータ（DataFrame形式）を生成
        if 'watcher4' in f:
            df = cg.getData(path)
            df['type'] = '現状'
        elif 'watcher5' in f:
            df = cs.getData(path)
            df['type'] = '先行き'
            df['Reason'] = np.nan
        else:
            continue

        # その他の情報を追加
        df['year'] = y
        df['month'] = m

        # データベースへ保存
        df.to_sql('data', conn, index=False, if_exists='append')

    # 結果を表示
    df_sql = pd.read_sql('select * from data', conn)
    print(df_sql)

    # csv形式で保存
    df_sql.to_csv('data.csv', encoding="Shift-JIS")

    # データベースをクローズ
    conn.close()

if __name__ == '__main__':
    main()
