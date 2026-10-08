このリポジトリはTEKKEN MANIAXの開発用リポジトリです。  
ポートフォリオ用に現在は公開しています。

使用言語:python 3.10
Webフレームワーク :Django　4.2.4
データベース MySQL
データストア: Redis

VideoとStreamの情報はYoutube Data APIとTwitch APIを使って、オンラインからデータを取得しています。
Youtube Video関連の情報はMySQLのvideoテーブルに保存しています。
Stream関係は取得してそのまま破棄するデータのため、Redisを利用しています。

