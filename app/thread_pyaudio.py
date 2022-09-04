import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

import globalVariables

class ThreadPyaudio(threading.Thread):
    def __init__(self, v=""):
        threading.Thread.__init__(self)
        self.kill_flag = False
        self.SAMPLING_RATE = globalVariables.SAMPLING_RATE
        self.CHANNELS = 1
        self.CHUNK = globalVariables.CHUNK
        self.INPUT_DEVICE_INDEX = globalVariables.INPUT_DEVICE_INDEX
        self.OUTPUT_DEVICE_INDEX = globalVariables.OUTPUT_DEVICE_INDEX
        self.FORMAT = pyaudio.paFloat32

    def callback(self, in_data, frame_count, time_info, status):
        output_buff = self.signal_proc(in_data)
        return (output_buff, pyaudio.paContinue)


    def signal_proc(self, input_buff, dtype=np.float32):
        input_data = np.frombuffer(input_buff, dtype=dtype)
        output_data = np.zeros((self.CHANNELS, self.CHUNK))
        output_data[0] = input_data

        output_data = np.reshape(output_data.T, (self.CHUNK * self.CHANNELS))
        wav_shift = pyrb.pitch_shift(output_data, self.SAMPLING_RATE, globalVariables.N_STEPS)
        output_buff = wav_shift.astype(dtype).tobytes()
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
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        p.terminate()

