# スマートハンガー

静電容量センサーで洗濯物の乾燥状態を監視し、乾燥時にLINEへ通知するIoTシステムです。

また、気象APIを用いて降雨を検知し、雨が降り始めた場合にはサーボモータでカバーを自動で展開して洗濯物を保護します。カバー作動後はLINEへ通知します。

Arduinoで取得したセンサーデータをPythonサーバで解析し、乾燥判定・降雨判定・通知・モーター制御を行う構成になっています。

## 機能

### 乾燥検知

静電容量センサーで洗濯物の状態を計測し、乾燥時にLINEへ通知します。

### 洗濯物の保護
[Yahooの気象情報API](https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html)を用いて降雨情報を取得します。雨を検知した場合はサーボモータで雨カバーを展開し、洗濯物を保護します。カバー作動後は、洗濯物を保護したことをLINEへ通知します。

### 手動操作
iPhoneショートカットから手動で雨カバーをかけることができます。

## システム構成
<img width="401" height="83" alt="Image" src="https://github.com/user-attachments/assets/a19b1f35-4393-4478-9375-a2b81de20733" />

### 動作フロー

1. Arduino が静電容量を測定し、TCP 通信でサーバーに `時間`・`容量` を送信します。
2. サーバーが 20 回分のデータを蓄積し、状態を判定します。
   - 雨検知： Yahoo天気APIで 降水量 > 0 の場合は雨と判定します。  `MOTOR` コマンドをArduinoへ送信し、LINEへ通知します。

   - 乾燥完了: 時定数 < 200 μs の回数が 20 回中 8 回以上の場合、乾燥完了と判定してLINEへ通知します。

3. Arduinoが `MOTOR` コマンドを受信すると、サーボモータを回転させて洗濯物にカバーをかぶせます。

## ディレクトリ構成

```text
smart-hanger/
├── src/
│   ├── Arduino/
│   │   ├── r4wifi.ino                # Arduino
│   │   ├── config.h                  # WiFi・サーバ・API設定（Git管理外）
│   │   └── test/                     # Arduino用のテストコード
│   ├── server/
│   │   ├── main_server.py            # メインサーバ
│   │   └── test/                     # サーバのテストコード
│   └── plot.py                       # 測定データの可視化                       
├── data/
│   ├── SmartHanger.drawio.png        
│   ├── capacity.csv                  # 測定データ
│   ├── capacity.png                  # 測定データの可視化結果
│   └── electrode_test/    
├── README.md                        
├── requirements.txt                 
├── LICENSE 
└── .gitignore             
```

## 主要ファイル構成

| ファイル | 役割 |
| --- | --- |
| `src/Arduino/r4wifi.ino` | Arduino側のプログラム。静電容量の測定、TCP通信によるデータ送信、サーボモータ制御を行います。|
| `src/server/main_server.py` | Pythonサーバ側のプログラム。測定値の受信、乾燥判定・降雨判定、LINE通知、Arduinoへの制御指示を行います。|

## セットアップ

### 必要なもの

- **ハードウェア**
    - Arduino UNO R4 WiFi 
    - サーボモータ
    - 静電容量センサー回路

- **開発環境**
    - Python 3.13.3
    - Arduino IDE

- **外部API**
    - LINE Notify トークン（ 2025 年 3 月終了 ） 
    - Yahoo天気API appid

### サーバ側
サーバを起動します。

```bash
python src/server/main_server.py
```

### Arduino側
Arduino UNO R4 WiFi へ `src/Arduino/r4wifi.ino` を書き込みます。