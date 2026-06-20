# スマートハンガー

静電容量センサーで洗濯物の乾燥状態を監視し、乾燥時にはLINEに通知するIoTシステムです。

また、気象APIを用いて降雨を検知し、雨が降り始めた場合にはサーボモーターでカバーを自動で展開し、洗濯物を保護します。その後、カバーを作動させたことをLINEに通知します。

Arduinoで取得したセンサーデータをPythonサーバーで解析し、乾燥判定・雨判定・通知・モーター制御を行う構成になっています。

## 機能

### 乾燥検知
静電容量センサーで洗濯物の状態を計測し、乾燥時にLINE通知します。

### 洗濯物の保護
[Yahooの気象情報API](https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html)を用いて降雨状態を取得します。雨が降り始めた場合はサーボモーターで雨カバーを展開し、洗濯物を保護します。また、洗濯物に雨カバーをかけたことをLINEに通知します。

### 手動操作
iPhoneショートカットから手動で雨カバーをかけることができます。

## システム構成
<img width="401" height="83" alt="Image" src="https://github.com/user-attachments/assets/a19b1f35-4393-4478-9375-a2b81de20733" />

### 動作フロー

1. Arduino が静電容量を測定し、TCP でサーバーに `時間,容量` を送信
2. サーバーが20回分のデータを蓄積し、以下を判定：
   - **雨検知**： Yahoo天気API で降水量 > 0 → `MOTOR` コマンドを返信 + LINE通知
   - **乾燥完了**: 時定数 < 200μs が 20回中 8回以上 → LINE通知
3. Arduino が `MOTOR` コマンドを受信するとサーボモーターを回転させ、洗濯物にカバーをかける

## ディレクトリ構成

```text
smart-hanger/
├── src/
│   ├── Arduino/
│   │   ├── r4wifi.ino                # Arduino
│   │   ├── config.h                  # WiFi・サーバー・API設定（Git管理外）
│   │   └── test/                     # Arduino用のテストコード
│   ├── server/
│   │   ├── main_server.py            # メインサーバー
│   │   └── test/                     # サーバーのテストコード
│   └── plot.py                       # 測定データの可視化化                       
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
| `src/Arduino/r4wifi.ino` | Arduino 用のプログラム。静電容量測定、TCP 送信、サーボ制御を行います。 |
| `src/server/main_server.py` | Python サーバー。測定値受信、乾燥判定、雨判定、通知、手動操作受信を行います。 |

## セットアップ

### 必要なもの

- **ハードウェア**
    - Arduino UNO R4 WiFi 
    - サーボモーター 
    - 静電容量センサー回路
- **Python**
    - 3.13.3
- **外部API**
    - LINE Notify トークン（2025年3月終了） 
    - Yahoo天気API appid

### サーバー
サーバー起動：

```bash
python src/server/main_server.py
```

### Arduino
Arduino IDE で `src/Arduino/r4wifi.ino` を書き込み