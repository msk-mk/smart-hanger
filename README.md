# スマートハンガー

静電容量センサーで洗濯物の乾燥状態を監視し、雨が降り始めたらサーボモーターで自動でカバーをかけるIoTシステム。
衣服が乾いた際に通知する機能もあります。

## 機能
1. 洗濯物が乾いたとき
    - 洗濯物の静電容量を常時測定し、時定数が20回中8回以上200μs以下であった場合にLINEに通知

2. 雨が降り始めたとき
    - [Yahooの気象情報API](https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html) から指定した緯度経度の雨の強さを取得

    - 雨が降り始めたらLINEに通知

## システム構成


### 動作フロー

1. Arduino が静電容量を測定し、TCP でサーバーに `時間,容量` を送信
2. サーバーが20回分のデータを蓄積し、以下を判定：
   - **雨検知**: Yahoo天気APIで降水量 > 0 → `MOTOR` コマンドを返信 + LINE通知
   - **乾燥完了**: 時定数 < 200μs が 20回中 8回以上 → LINE通知
3. Arduino が `MOTOR` を受信するとサーボモーターを回転させ、洗濯物にカバーをかける

## ディレクトリ構成

```
BDM/
├── src/
│   ├── Arduino/
│   │   ├── r4wifi.ino          # デバイス
│   │   ├── config.h            # WiFi/サーバー/API設定（Git管理外）
│   │   └── test/
│   ├── server/
│   │   ├── main_server.py      # メインサーバー
│   │   └── test/
│   └── plot.py                 # 静電容量データの可視化
├── data/
│   ├── capacity.csv            # 測定データ
│   ├── capacity.png            # 可視化結果
│   └── electrode_test/ 
├── .env                        # 環境変数（Git管理外）
├── .gitignore
└── requirements.txt
```

## セットアップ

### 必要なもの

- **ハードウェア**: Arduino UNO R4 WiFi / サーボモーター / 静電容量センサー回路
- **Python**: 3.13.3
- **外部API**: LINE Notify トークン（2025年3月終了） / Yahoo天気API appid

### サーバー側
サーバー起動：

```bash
python src/server/main_server.py
```

### Arduino側
Arduino IDE で `src/Arduino/r4wifi.ino` を書き込み