import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

class ThreadPyaudio(threading.Thread):
    def __init__(self, sampling_rate, n, input_device_index, output_device_index, n_steps):
        threading.Thread.__init__(self)
        self.kill_flag = False
        self.sampling_rate = sampling_rate
        self.n = n
        self.chunk = 1024 * self.n
        self.channels = 1
        # 複数のマイク/スピーカーがある場合はここでINDEXを設定する
        self.input_device_index = input_device_index
        self.output_device_index = output_device_index
        # 音声データフォーマット
        self.format = pyaudio.paFloat32 # Float 32bit mode
        # キー
        self.n_steps = n_steps
    
    def callback(self, in_data, frame_count, time_info, status):
        output_buff = self.signal_proc(in_data)
        return (output_buff, pyaudio.paContinue)


    def signal_proc(self, input_buff, dtype=np.float32):
        # Convert framebuffer into nd-array
        input_data = np.frombuffer(input_buff, dtype=dtype)
        
        # Signal processing
        # Set output as L-ch
        output_data = np.zeros((self.channels, self.chunk))
        output_data[0] = input_data

        # Pitch shift and Convert nd-array into framebuffer
        output_data = np.reshape(output_data.T, (self.chunk * self.channels))
        wav_shift = pyrb.pitch_shift(output_data, self.sampling_rate, self.n_steps)
        output_buff = wav_shift.astype(dtype).tobytes()
        return output_buff
    
    def run(self):
        """音声入出力ストリームの初期化"""
        p = pyaudio.PyAudio()

        # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
        # input_device_indexとoutput_device_indexを書き換える
        for x in range(0, p.get_device_count()):
            print(p.get_device_info_by_index(x))
            print("\n")

        stream = p.open( 
            format = self.format,
            channels = self.channels,
            rate = self.sampling_rate,
            frames_per_buffer = self.chunk,
            input = True,
            output = True,
            input_device_index = self.input_device_index,
            output_device_index = self.output_device_index,
            stream_callback = self.callback,
        )

        while stream.is_active() and not(self.kill_flag):
            time.sleep(0)
            
        stream.stop_stream()
        stream.close()
        p.terminate()

