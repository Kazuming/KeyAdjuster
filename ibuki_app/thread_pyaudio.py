import pyaudio
import numpy as np
import pyrubberband as pyrb
import threading
import time

class ThreadPyaudio(threading.Thread):
    def __init__(self, samplingRate, n, inputDeviceIndex, outputDeviceIndex, key):
        threading.Thread.__init__(self)
        self.killFlag = False
        self.samplingRate = samplingRate
        self.n = n
        self.chunk = 1024 * self.n
        self.channels = 1
        # 複数のマイク/スピーカーがある場合はここでINDEXを設定する
        self.inputDeviceIndex = inputDeviceIndex
        self.outputDeviceIndex = outputDeviceIndex
        # 音声データフォーマット
        self.format = pyaudio.paFloat32 # Float 32bit mode
        # キー
        self.key = key
    
    def callback(self, inData, frame_count, time_info, status):
        outputBuff = self.signalProc(inData)
        return (outputBuff, pyaudio.paContinue)


    def signalProc(self, inputBuff, dtype=np.float32):
        # Convert framebuffer into nd-array
        inputData = np.frombuffer(inputBuff, dtype=dtype)
        
        # Signal processing
        # Set output as L-ch
        outputData = np.zeros((self.channels, self.chunk))
        outputData[0] = inputData

        # Pitch shift and Convert nd-array into framebuffer
        outputData = np.reshape(outputData.T, (self.chunk * self.channels))
        wavShift = pyrb.pitch_shift(outputData, self.samplingRate, self.key)
        outputBuff = wavShift.astype(dtype).tobytes()
        return outputBuff
    
    def run(self):
        """音声入出力ストリームの初期化"""
        p = pyaudio.PyAudio()

        # 複数のマイク/スピーカーがある場合、以下のfor文で確認して
        # inputDeviceIndexとoutputDeviceIndexを書き換える
        for x in range(0, p.get_device_count()):
            print(p.get_device_info_by_index(x))
            print("\n")

        stream = p.open( 
            format = self.format,
            channels = self.channels,
            rate = self.samplingRate,
            frames_per_buffer = self.chunk,
            input = True,
            output = True,
            input_device_index = self.inputDeviceIndex,
            output_device_index = self.outputDeviceIndex,
            stream_callback = self.callback,
        )

        while stream.is_active() and not(self.killFlag):
            time.sleep(0)
            
        stream.stop_stream()
        stream.close()
        p.terminate()

