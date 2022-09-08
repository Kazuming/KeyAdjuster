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
        self.inputQ = []
        self.outputQ = []
        self.CHUNNELS = min(gv.INPUT_CHANNELS, gv.OUTPUT_CHANNELS)
        self.CHUNK = int(gv.SAMPLING_RATE/2)
        delay = np.zeros(self.CHUNK*self.CHUNNELS).reshape(-1, self.CHUNNELS)
        self.outputQ.append(delay)
        self.thread = threading.Thread(target=self.audio, daemon=True)
        self.thread.start()
        # Start, Stopを高速に繰り返したとき、streamを開く前に閉じてしまうエラーに対処
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
            channels = self.CHUNNELS,
            rate = gv.SAMPLING_RATE,
            frames_per_buffer = self.CHUNK,
            input = True,
            output = True,
            input_device_index = gv.INPUT_DEVICE_INDEX,
            output_device_index = gv.OUTPUT_DEVICE_INDEX,
            stream_callback = self.callback
            )
        self.stream.start_stream()
        data = np.zeros(self.CHUNK*2).reshape(-1, self.CHUNNELS)
        while self.stream.is_active():
            if len(self.inputQ) == 0:
                time.sleep(0.1)
                continue
            data = self.signal_proc(data)

    def callback(self, in_data, frame_count, time_info, status):
        self.inputQ.append(in_data)
        if len(self.outputQ) == 0:
            delay = np.zeros(self.CHUNK*self.CHUNNELS).reshape(-1, self.CHUNNELS)
            self.outputQ.append(delay)
        return (self.outputQ.pop(0), pyaudio.paContinue)

    def signal_proc(self, take_over):
        input_data = np.frombuffer(self.inputQ.pop(0), dtype=np.float32)
        input_data = input_data.reshape(-1, self.CHUNNELS)
        base_data = np.concatenate([take_over, input_data], 0)
        shift_data = pyrb.pitch_shift(base_data, gv.SAMPLING_RATE, gv.N_STEPS)[self.CHUNK:self.CHUNK*2]
        output_data = shift_data.astype(np.float32).tobytes()
        self.outputQ.append(output_data)
        return base_data[self.CHUNK:]

    def stop(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            threading.Event().clear()
        except AttributeError:
            pass
