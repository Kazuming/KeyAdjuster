import matplotlib
matplotlib.use('Qt5Agg')

import pyaudio
import numpy as np
import threading
import codecs
from pylab import *
import time


######### ここからパラメータ設定
# データ送受信に使用する音の周波数設定
# （Frequency Shift Keyingで変調するので2種類使う）
FREQUENCY0 = 2500
FREQUENCY1 = 3500
# 送受信ビットレート（bit per second）
# （マンチェスター符号が有効の場合実効レートは半分になる）
BPS = 50
# マンチェスタ符号化有無
IS_MANCHESTER = True

# 再生音量（最大1.0）
VOLUME = 0.7
# 複数のマイク/スピーカーがある場合はここでINDEXを設定する
INPUT_DEVICE_INDEX = 0
OUTPUT_DEVICE_INDEX = 1
# 録音データを（CHUNK/SAMPLING_RATE）秒ごとに処理する
# CHUNK = 32768 #for Win10
CHUNK = 8192 #for MacOS
# 再生/録音サンプリングレート
SAMPLING_RATE = 48000             # sampling frequency [Hz]
# 再生チャネル （多分変更しなくて良い）
CHANNELS = 1             # monaural
# 音声データフォーマット
FORMAT = pyaudio.paFloat32 # Float 32bit mode
#FORMAT = pyaudio.paInt16 # Int 16bit mode, 演算を軽くしたいとき用

# デバッグ用（録音データ保存）
DEBUG_MODE = False
#DEBUG_MODE = True

IS_PLOT = True
DOWNSAMPLE = 8
PLOT_LEN = int(65536 / CHUNK)
######### ここまでパラメータ設定

def pyaudio_init():
    """音声入出力ストリームの初期化"""
    paudio = pyaudio.PyAudio()

    # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
    # INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
    for x in range(0, paudio.get_device_count()): 
        print(paudio.get_device_info_by_index(x))
        print("\n")


    inputstream = paudio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    outputstream = paudio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    output=True,
                    output_device_index=OUTPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    return paudio, inputstream, outputstream

if __name__ == "__main__":
    pyaudio_init()