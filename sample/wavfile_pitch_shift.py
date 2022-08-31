import pyaudio
import wave
import librosa


######### ここからパラメータ設定
# 再生チャネル （多分変更しなくて良い）
CHANNELS = 1             # monaural
# 音声データフォーマット
FORMAT = pyaudio.paFloat32 # Float 32bit mode
# 再生/録音サンプリングレート
SAMPLING_RATE = 44100         # sampling frequency [Hz]
# 複数のマイク/スピーカーがある場合はここでINDEXを設定する
INPUT_DEVICE_INDEX = 0
OUTPUT_DEVICE_INDEX = 1
# 録音データを（CHUNK/SAMPLING_RATE）秒ごとに処理する
CHUNK = 2**10

record_time = 5
input_path = "./input_data/input.wav"

def pyaudio_init():
    """音声入出力ストリームの初期化"""
    paudio = pyaudio.PyAudio()

    # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
    # INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
    for x in range(0, paudio.get_device_count()):
        print(paudio.get_device_info_by_index(x))
        print("\n")

    return paudio

# 録音
def record():
    inputstream = paudio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    print("Recording ...")
    frames = []
    for i in range(0, int(SAMPLING_RATE / CHUNK * record_time)):
        data = inputstream.read(CHUNK)
        frames.append(data)
    print("Done.")
    inputstream.stop_stream()
    inputstream.close()

    wf = wave.open(input_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(paudio.get_sample_size(FORMAT))
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 再生
def play(paudio, wavfile_path):
    wf = wave.open(wavfile_path, 'rb')
    outputstream = paudio.open(format=paudio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        outputstream.write(data)
        data = wf.readframes(CHUNK)
    
    outputstream.stop_stream()
    outputstream.close()

# キー変更
def key_adjuster(inputfile_path, outputfile_path, n_steps):
    wav, sr = librosa.load(inputfile_path, SAMPLING_RATE)
    print(f'wav: {wav}')
    wav_shift = librosa.effects.pitch_shift(wav, sr, n_steps)
    print(f'wav_shift: {wav_shift}')

    wf = wave.open(outputfile_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(paudio.get_sample_size(FORMAT))
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b''.join(wav_shift))
    wf.close()

if __name__ == "__main__":
    # スピーカーとマイクによる入出力を設定
    paudio = pyaudio_init()

    # 録音
    # record()

    # キー変更
    # key_adjuster("./input_data/input.wav", "./output_data/music.wav", -2)
    key_adjuster("./input_data/sinjidai.wav", "./output_data/music.wav", 2)

    # 再生
    # play(paudio, "./input_data/input.wav")
    # play(paudio, "./input_data/sinjidai.wav")
    play(paudio, "./output_data/music.wav")

    paudio.terminate()
