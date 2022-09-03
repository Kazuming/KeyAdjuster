import pyaudio
import numpy as np
import librosa
import pyrubberband as pyrb
import time


SAMPLING_RATE = 44100
N = 50
CHUNK = 1024*N
CHANNELS = 1
# 複数のマイク/スピーカーがある場合はここでINDEXを設定する
INPUT_DEVICE_INDEX = 3
OUTPUT_DEVICE_INDEX = 1
# 音声データフォーマット
FORMAT = pyaudio.paFloat32 # Float 32bit mode
N_STEPS = 0


def pyaudio_init():
    """音声入出力ストリームの初期化"""
    p = pyaudio.PyAudio()
    global N_STEPS

    # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
    # INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
    for x in range(0, p.get_device_count()):
        print(p.get_device_info_by_index(x))
        print("\n")

    stream = p.open( 
        format=FORMAT,
        channels=CHANNELS,
        rate = SAMPLING_RATE,
        frames_per_buffer=CHUNK,
        input = True,
        output=True,
        input_device_index=INPUT_DEVICE_INDEX,
        output_device_index=OUTPUT_DEVICE_INDEX,
        stream_callback = callback,
    )

    while stream.is_active():
        kb = int(input())
        if type(kb) == int:
            N_STEPS = kb
        time.sleep(0)
        
    stream.stop_stream()
    stream.close()
    p.terminate()


def callback(in_data, frame_count, time_info, status):
    output_buff = signal_proc(in_data)
    return (output_buff, pyaudio.paContinue)


def signal_proc(input_buff, dtype=np.float32):
    # Convert framebuffer into nd-array
    input_data = np.frombuffer(input_buff, dtype=dtype)
    
    # Signal processing
    # Set output as L-ch
    output_data = np.zeros((CHANNELS, CHUNK))
    output_data[0] = input_data

    # Pitch shift and Convert nd-array into framebuffer
    output_data = np.reshape(output_data.T, (CHUNK * CHANNELS))
    # wav_shift = librosa.effects.pitch_shift(y=output_data, sr=SAMPLING_RATE, n_steps=N_STEPS)
    wav_shift = pyrb.pitch_shift(output_data, SAMPLING_RATE, N_STEPS)
    output_buff = wav_shift.astype(dtype).tobytes()
    return output_buff


if __name__ == "__main__":
    pyaudio_init()
