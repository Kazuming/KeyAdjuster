import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

import globalVariables as gv


class ThreadPyaudio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pa = pyaudio.PyAudio()
        self.CHANNELS = min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS)

    def callback(self, in_data, frame_count, time_info, status):
        output_buff = self.signal_proc(in_data)
        return (output_buff, pyaudio.paContinue)

    def signal_proc(self, input_buff, dtype=np.float32):
        input_data = np.frombuffer(input_buff, dtype=dtype)
        input_data = input_data.reshape(-1, self.CHANNELS)
        wav_shift = pyrb.pitch_shift(input_data, gv.SAMPLING_RATE, gv.N_STEPS)
        output_buff = wav_shift.astype(np.float32).tobytes()
        return output_buff

    def run(self):
        """音声入出力ストリームの初期化"""
        self.stream = self.pa.open(
            format = pyaudio.paFloat32,
            channels = min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS),
            rate = gv.SAMPLING_RATE,
            frames_per_buffer = gv.CHUNK*1024,
            input = True,
            output = True,
            input_device_index = gv.INPUT_DEVICE_INDEX,
            output_device_index = gv.OUTPUT_DEVICE_INDEX,
            stream_callback = self.callback,
        )
        while self.stream.is_active():
            time.sleep(0)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

