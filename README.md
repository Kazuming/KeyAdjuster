# Key Adjuster
 
カラオケで、自分に合ったキーがわからない人が、手軽に原曲のキーを変更して練習できるアプリケーションです。
PC上で再生中の音を入力として、リアルタイムにキーを変更して出力します。
 
# デモ動画
<div align="center">
 <video src="https://user-images.githubusercontent.com/104568924/190580710-7b7d9088-ac8d-4842-84fa-e70c79b70dc5.mov"></video>
</div>
 
# アプリの特徴
 
* リアルタイムでキー変更を行うので、音楽ファイルなどの準備が不要です。
* 入出力の処理を並列化することで、音質を下げずにキー変更を可能にしました。
* 誰もが使いやすいように、シンプルなUIに設計しました。
 
# インストール手順

## Mac用
### Homebrewのインストール
<a href="https://brew.sh/index_ja">Homebrewのホームーページ</a>

### ライブラリのインストール

```bash
$ brew update
$ brew install rubberband
$ brew install portaudio 
```
### 仮想デバイスのインストール

- Intelチップ搭載のMacbookの方
<br>Soundflower: https://soundflower.softonic.jp/mac

- M1チップ搭載のMacbookの方
<br>Blackhole: https://existential.audio/blackhole/?pk_campaign=github&pk_kwd=readme

### Key Adjusterのダウンロード
https://github.com/Kazuming/KeyAdjuster/releases/download/v1.0.0/KeyAdjuster_for_Mac.zip

### PCで流せる音楽アプリ
YouTube、Apple Musicなど

## Windows用

### ライブラリ（rubberband）のインストール
#### rubberband: <a href="https://www.wizard-notes.com/entry/python/pyrubberband">参考資料</a>

### 仮想デバイスのインストール
#### VB-CABLE: <a href="https://arutora.com/15923">参考資料</a>
インストール後、Windowsの設定→システム→サウンドから、出力デバイスのところに「CABLE Input」、入力デバイスのところに「CABLE Output」をセット
してください。

### Key Adjusterのダウンロード
https://github.com/Kazuming/KeyAdjuster/releases/download/v1.0.0/KeyAdjuster_for_Windows.zip

### PCで流せる音楽アプリ
YouTube、Apple Musicなど

# 利用方法
1. ダウンロードしたKeyAdjusterを開く(アプリ立ち上げに20秒ほどかかります)
2. PCのサウンド出力を仮想デバイスに変更
3. KeyAdjusterのInput Deviceを仮想デバイス、Output Deviceを出力したい機器(イヤホン、スピーカなど)に変更
4. 音楽アプリを再生
5. KeyAdjusterのSTARTボタンを押し、キー変更スタート

※わからない方はデモ動画をご覧ください。
 
# 作成者
 
* 作成者: 成川伊吹、木村和真、佐藤正和
* E-mail:mgmgmtww@gmail.com
