from bs4 import BeautifulSoup as BsObj
from urllib import request
from urllib.error import HTTPError

"""
内閣府HPから景気判断理由集のcsv（期間:2000年1月〜最新）をダウンロードし、CSVFilesフォルダ以下に保存。
"""

def get_allurl(target):
    # webページ内の全urlを取得する関数
    _url = target
    data = request.urlopen(_url).read()
    text = data.decode("utf-8")
    soup = BsObj(data, 'html.parser')
    links = soup.find_all("a")
    link_list = []
    for a in links:
        try:
            href = a.attrs['href']
            link_list.append(href)
        except:
            continue
    return link_list

def main():

    # 2010年以降のデータのリンクを取得
    urls = get_allurl('http://www5.cao.go.jp/keizai3/watcher_index.html')
    urls = urls + get_allurl('http://www5.cao.go.jp/keizai3/kako_watcher.html')

    # 景気判断理由の現状（watcher4）と先行き（watcher5）をダウンロードし、yyyymmddwatcherX.csvとして保存
    for u in urls:
        if 'watcher/menu.html' in u:
            d = u[:9].replace('/','')
            _u4 = 'http://www5.cao.go.jp/keizai3/' + u[:9] + 'watcher/watcher4.csv'
            _u5 = 'http://www5.cao.go.jp/keizai3/' + u[:9] + 'watcher/watcher5.csv'
            try:
                request.urlretrieve(_u4, 'CSVFiles/' + d[:6] + 'watcher4.csv')
                request.urlretrieve(_u5, 'CSVFiles/' + d[:6] + 'watcher5.csv')
                print(_u4)
                print(_u5)
            except HTTPError:
                continue

    # 2009年以前のデータのリンクを取得
    urls3 = get_allurl('http://www5.cao.go.jp/keizai3/kako_csv/kako2_watcher.html')

    # 2012年以降のデータと同様の形式で保存
    for u in urls3:
        if '_watcher4.csv' in u or '_watcher5.csv' in u:
            d = u[1:5]
            _d = str(2000 + int(u[1:3]) - 12) + str(u[3:5])
            _u4 = 'http://www5.cao.go.jp/keizai3/kako_csv/h' + d + '_watcher4.csv'
            _u5 = 'http://www5.cao.go.jp/keizai3/kako_csv/h' + d + '_watcher5.csv'
            try:
                request.urlretrieve(_u4, 'CSVFiles/' + _d + 'watcher4.csv')
                request.urlretrieve(_u5, 'CSVFiles/' + _d + 'watcher5.csv')
                print(_u4)
                print(_u5)
            except HTTPError:
                continue

if __name__ == '__main__':
    main()
