import pyaudio
import wave
import serial
import threading
import os
import sys
from random import randint

available = True

if len(sys.argv) >= 2:  # check if a com port has been given as argument, else take com 6
    port = sys.argv[1]
else:
    port = '/dev/ttyUSB0'

print("port = " + port)
baud = 115200
try:
    serial_port = serial.Serial(port, baud, timeout=0)
except:
    sys.exit("Unable to establish connection at COM port")

CHUNK = 1024
audio_file_path = os.path.dirname(os.path.abspath(__file__)) + r"/audio/"  # r"C:\Users\bramd\Desktop\MTBE\Lotte\\"

files = ['01_plakband.wav', '02_WHscream.wav', '03_godveredomme.wav', '04_FACK.wav', '05_FAAAAAACK.wav']
errorFiles = ['toSmall.wav', 'toBig.wav']


def read_serial(ser):
    global available
    if ~available:
        return
    print("Reading.....")
    while available:
        reading = ser.readline().decode("utf-8")
        if reading != '':
            print(reading)
        if 'BIEM' in reading:
            print("DING!")
            selected = randint(0, len(files) - 1)
            print(selected)
            play(audio_file_path + files[selected])


def play(audio_file):
    global available
    available = False
    wf = wave.open(audio_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    available = True


thread = threading.Thread(target=read_serial, args=(serial_port,))
thread.start()
