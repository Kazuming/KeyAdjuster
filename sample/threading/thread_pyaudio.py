import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

class ThreadPyaudio(threading.Thread):
    def __init__(self, v=""):
        threading.Thread.__init__(self)
        self.kill_flag = False
        self.SAMPLING_RATE = 44100
        self.N = 50
        self.CHUNK = 1024*self.N
        self.CHANNELS = 1
        # 複数のマイク/スピーカーがある場合はここでINDEXを設定する
        self.INPUT_DEVICE_INDEX = 3
        self.OUTPUT_DEVICE_INDEX = 1
        # 音声データフォーマット
        self.FORMAT = pyaudio.paFloat32 # Float 32bit mode
        # キー
        self.N_STEPS = 0
    
    def callback(self, in_data, frame_count, time_info, status):
        output_buff = self.signal_proc(in_data)
        return (output_buff, pyaudio.paContinue)


    def signal_proc(self, input_buff, dtype=np.float32):
        # Convert framebuffer into nd-array
        input_data = np.frombuffer(input_buff, dtype=dtype)
        
        # Signal processing
        # Set output as L-ch
        output_data = np.zeros((self.CHANNELS, self.CHUNK))
        output_data[0] = input_data

        # Pitch shift and Convert nd-array into framebuffer
        output_data = np.reshape(output_data.T, (self.CHUNK * self.CHANNELS))
        wav_shift = pyrb.pitch_shift(output_data, self.SAMPLING_RATE, self.N_STEPS)
        output_buff = wav_shift.astype(dtype).tobytes()
        return output_buff
    
    def run(self):
        """音声入出力ストリームの初期化"""
        p = pyaudio.PyAudio()

        # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
        # INPUT_DEVICE_INDEXとOUTPUT_DEVICE_INDEXを書き換える
        for x in range(0, p.get_device_count()):
            print(p.get_device_info_by_index(x))
            print("\n")

        stream = p.open( 
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.SAMPLING_RATE,
            frames_per_buffer = self.CHUNK,
            input = True,
            output = True,
            input_device_index = self.INPUT_DEVICE_INDEX,
            output_device_index = self.OUTPUT_DEVICE_INDEX,
            stream_callback = self.callback,
        )

        while stream.is_active() and not(self.kill_flag):
            time.sleep(0)
            
        stream.stop_stream()
        stream.close()
        p.terminate()

