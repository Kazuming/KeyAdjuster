import pyaudio
import numpy as np
import librosa
import time

RATE = 44100
CHUNK = 1024
CHANNELS = 1
# 複数のマイク/スピーカーがある場合はここでINDEXを設定する
INPUT_DEVICE_INDEX = 2
OUTPUT_DEVICE_INDEX = 1
# 音声データフォーマット
FORMAT = pyaudio.paFloat32 # Float 32bit mode

def signal_proc(input_buff, dtype=np.float32):
    # Convert framebuffer into nd-array
    input_data = np.fromstring(input_buff, dtype=dtype)
    
    # Signal processing
    # Set output as L-ch
    output_data = np.zeros((CHANNELS, CHUNK))
    output_data[0] = input_data

    # Convert nd-array into framebuffer
    output_data = np.reshape(output_data.T, (CHUNK * CHANNELS))
    wav_shift = librosa.effects.pitch_shift(output_data, RATE, 1)
    output_buff = wav_shift.astype(dtype).tobytes()
    return output_buff


p = pyaudio.PyAudio()
def callback(in_data, frame_count, time_info, status):
    # input_buff = stream.read(CHUNK)
    output_buff = signal_proc(in_data)
    return (output_buff, pyaudio.paContinue)

# 複数のマイク/スピーカーがある場合、以下のfor文で確認して
# INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
for x in range(0, p.get_device_count()):
    print(p.get_device_info_by_index(x))
    print("\n")

stream = p.open( 
        format=FORMAT,
        channels=CHANNELS,
        rate = RATE,
        frames_per_buffer=CHUNK,
        input = True,
        output=True,
        input_device_index=INPUT_DEVICE_INDEX,
        output_device_index=OUTPUT_DEVICE_INDEX,
        stream_callback = callback,
    )

while stream.is_active():
    time.sleep(0.01)
    
stream.stop_stream()
stream.close()
p.terminate()
