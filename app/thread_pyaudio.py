import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

import globalVariables
import asyncio

class ThreadPyaudio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.CHANNELS = 2
        self.FORMAT = pyaudio.paFloat32
        self.INPUT_DEVICE_INDEX = globalVariables.INPUT_DEVICE_INDEX
        self.OUTPUT_DEVICE_INDEX = globalVariables.OUTPUT_DEVICE_INDEX
        self.SAMPLING_RATE = globalVariables.SAMPLING_RATE
        self.CHUNK = globalVariables.CHUNK*1024
        self.kill_flag = False


    def callback(self, in_data, frame_count, time_info, status):
        output_buff = self.signal_proc(in_data)
        return (output_buff, pyaudio.paContinue)


    def signal_proc(self, input_buff, dtype=np.float32):
        input_data = np.frombuffer(input_buff, dtype=dtype)
        input_data = input_data.reshape(-1, self.CHANNELS)
        wav_shift = pyrb.pitch_shift(input_data, self.SAMPLING_RATE, globalVariables.N_STEPS)
        output_buff = wav_shift.astype(np.float32).tobytes()
        return output_buff


    def run(self):
        """音声入出力ストリームの初期化"""
        p = pyaudio.PyAudio()
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

