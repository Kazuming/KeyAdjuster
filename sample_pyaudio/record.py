import pyaudio
import wave
 
CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
record_time = 5
output_path = "./output.wav"
 
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
 
print("Recording ...")
frames = []
for i in range(0, int(RATE / CHUNK * record_time)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done.")
 
stream.stop_stream()
stream.close()
p.terminate()
 
wf = wave.open(output_path, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
