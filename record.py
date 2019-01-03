import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6  # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 1.2

WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()

stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = []

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    # Do dome thing with the chunk data, run any speech processing on-the-fly
    d = np.fromstring(data, dtype=np.int16)
    np.save(str('o_all'), d)
    ch0 = d[np.arange(0, CHUNK, 6)]
    ch1 = d[np.arange(1, CHUNK, 6)]
    ch2 = d[np.arange(2, CHUNK, 6)]
    ch3 = d[np.arange(3, CHUNK, 6)]
    ch4 = d[np.arange(4, CHUNK, 6)]
    ch5 = d[np.arange(5, CHUNK, 6)]


print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()
