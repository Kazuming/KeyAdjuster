import pyaudio
import wave

CHUNK_SIZE = 2**10
sr = 44100

wf = wave.open('src/sinjidai.wav', 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                # rate=wf.getframerate(),
                rate=sr,
                output=True)

data = wf.readframes(CHUNK_SIZE)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK_SIZE)
    print(data)

stream.stop_stream()
stream.close()
p.terminate()