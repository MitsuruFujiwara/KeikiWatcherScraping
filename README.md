# KeikiWatcherScraping
景気ウォッチャー調査の景気判断理由集をスクレイピングするやつ

内閣府が毎月発表している景気ウォッチャー調査の景気判断理由集のcsvデータを取得し、データベースを生成するためのスクリプト。  
景気ウォッチャー調査：http://www5.cao.go.jp/keizai3/watcher/watcher_menu.html

### 使い方
Scraping.pyの実行でCSVFilesフォルダ以下に景気判断理由集のcsvファイルが保存される。  
その後DataBase.pyを実行することでsqlite3形式のデータベース（data.db）とcsv形式のテキストデータ（data.csv）が生成される。

### スクリプトを実行するにあたって必要なパッケージ
numpy, pandas, beautifulsoup4  

python 3.5.2で動作確認済
