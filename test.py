import pyaudio
import time
import librosa
import wave
import soundcard as sc
import soundfile as sf


FORMAT = pyaudio.paInt16
CHUNK= 2**10
CHANNELS = 1
SAMPLING_RATE = 240000
INPUT_DEVICE_INDEX = 3
OUTPUT_DEVICE_INDEX = 1


p = pyaudio.PyAudio()
def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

out_stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLING_RATE,
                output=True,
                output_device_index=OUTPUT_DEVICE_INDEX)



output_file_name = "out.wav"    # 出力するファイル名
samplerate = 192000              # サンプリング周波数 [Hz]
record_sec = 5                  # 録音する時間 [秒]

with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate) as mic:
    # デフォルトスピーカーから録音
    while True:
        try:
            # TODO 並列化
            data = mic.record(numframes=samplerate).tobytes()
            out_stream.write(data)

        except KeyboardInterrupt: ## ctrl+c で終了
            break

    # マルチチャンネルで保存したい場合は、"data=data[:, 0]"を"data=data"に変更
    sf.write(file=output_file_name, data=data[:, 0], samplerate=samplerate)


p.terminate()