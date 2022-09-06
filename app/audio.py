import queue
import threading
import time

import numpy as np
import pyaudio
import pyrubberband as pyrb

import global_variables as gv


class ThreadPyaudio:

    def __init__(self):
        self.started = threading.Event()
        self.pa = pyaudio.PyAudio()

    def start(self):
        self.inputQ = queue.Queue(maxsize=8)
        self.outputQ = queue.Queue(maxsize=8)
        self.input_thread = threading.Thread(target=self.audio, daemon=True)
        self.input_thread.start()
        # Start, Stopを高速に繰り返したとき、streamが閉じられないエラーに対処
        while True:
            try:
                if self.stream.is_active():
                    break
                else:
                    time.sleep(0.1)
            except AttributeError:
                time.sleep(0.1)
            except OSError:
                time.sleep(0.1)

    def audio(self):
        self.stream = self.pa.open(
            format = pyaudio.paFloat32,
            channels = min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS),
            rate = gv.SAMPLING_RATE,
            frames_per_buffer = int(gv.DELAY*gv.SAMPLING_RATE/2),
            input = True,
            output = True,
            input_device_index = gv.INPUT_DEVICE_INDEX,
            output_device_index = gv.OUTPUT_DEVICE_INDEX,
            stream_callback = self.callback
            )
        self.stream.start_stream()
        while self.stream.is_active():
            if self.inputQ.empty():
                time.sleep(0.1)
                continue
            self.signal_proc()

    def callback(self, in_data, frame_count, time_info, status):
        # queueアクセス時に細かいノイズが発生
        if not self.inputQ.full():
            self.inputQ.put(in_data)
        if self.outputQ.empty():
            wait_data = np.zeros(int(gv.DELAY*gv.SAMPLING_RATE/2)).reshape(-1, min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS))
            self.outputQ.put(wait_data)
        return (self.outputQ.get(), pyaudio.paContinue)

    def signal_proc(self):
        input_data = np.frombuffer(self.inputQ.get(), dtype=np.float32)
        input_data = input_data.reshape(-1, min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS))
        shift_data = pyrb.pitch_shift(input_data, gv.SAMPLING_RATE, gv.N_STEPS*2)
        output_data = shift_data.astype(np.float32).tobytes()
        self.outputQ.put(output_data)

    def stop(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            threading.Event().clear()
        except AttributeError:
            pass
