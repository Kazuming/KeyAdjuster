import pyaudio
import numpy as np
import librosa

RATE = 44100
CHUNK = 2**10
CHANNEL_IN = 1
CHANNEL_OUT = 2
# 複数のマイク/スピーカーがある場合はここでINDEXを設定する
INPUT_DEVICE_INDEX = 2
OUTPUT_DEVICE_INDEX = 3

def signal_proc(input_buff, dtype=np.int16):
    # Convert framebuffer into nd-array
    input_data = np.fromstring(input_buff, dtype=dtype)
    
    # Signal processing
    # Set output as L-ch
    output_data = np.zeros((CHANNEL_OUT, CHUNK))
    output_data[0] = input_data

    # Convert nd-array into framebuffer
    output_data = np.reshape(output_data.T, (CHUNK * CHANNEL_OUT))
    # wav_shift = librosa.effects.pitch_shift(output_data, RATE, 2)
    # print(type(wav_shift))
    output_buff = output_data.astype(dtype).tobytes()
    return output_buff


p = pyaudio.PyAudio()
# 複数のマイク/スピーカーがある場合、以下のfor文で確認して
# INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
for x in range(0, p.get_device_count()):
    print(p.get_device_info_by_index(x))
    print("\n")

stream_in = p.open( 
        format=pyaudio.paInt16,
        channels=CHANNEL_IN,
        rate = RATE,
        frames_per_buffer=CHUNK,
        input = True,
        output = False,
        input_device_index=INPUT_DEVICE_INDEX,
    )

stream_out = p.open(    
        format=pyaudio.paInt16,
        channels=CHANNEL_OUT,
        rate=RATE,
        frames_per_buffer=CHUNK,
        input=False,
        output=True,
        output_device_index=OUTPUT_DEVICE_INDEX,
    )

while stream_in.is_active() and stream_out.is_active():
    input_buff = stream_in.read(CHUNK)
    output_buff = signal_proc(input_buff)
    stream_out.write(output_buff)
    
stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
p.terminate()
