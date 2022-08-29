import soundcard as sc
import soundfile as sf

output_file_name = "out.wav"    # 出力するファイル名
samplerate = 48000              # サンプリング周波数 [Hz]
record_sec = 5                  # 録音する時間 [秒]

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate) as mic:
    # デフォルトスピーカーから録音
    data = mic.record(numframes=samplerate*record_sec)

    # マルチチャンネルで保存したい場合は、"data=data[:, 0]"を"data=data"に変更
    sf.write(file=output_file_name, data=data[:, 0], samplerate=samplerate)