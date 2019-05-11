import pyaudio
import wave
import serial
import threading
import os
import sys
from random import randint

if len(sys.argv)>=2:    #check if a com port has been given as argument, else take com 6
    port = sys.argv[1]
else:
    port = 'ttyUSB0'

print("port = " + port)
baud = 115200
try:
    serial_port = serial.Serial(port, baud, timeout=0)
except:
    sys.exit("Unable to establish connection at COM port")

CHUNK = 1024
audio_file_path = os.path.dirname(os.path.abspath(__file__))+ r"\audio\\"       # r"C:\Users\bramd\Desktop\MTBE\Lotte\\"



files = ['0.wav', '1.wav', '2.wav', '3.wav', '4.wav', '5.wav', '6.wav', '7.wav', '8.wav', '9.wav', '10.wav',
         '11.wav', '12.wav', '13.wav', '14.wav', '15.wav', '16.wav', '17.wav', '18.wav', '19.wav', '20.wav',
         '21.wav', '22.wav', '23.wav', '24.wav', '25.wav', '26.wav', '27.wav', '28.wav', '29.wav', '30.wav']
errorFiles = ['toSmall.wav', 'toBig.wav']

def read_serial(ser):
    print("Reading.....")
    while True:
        reading = ser.readline().decode("utf-8")
        if reading != '':
             print(reading)
        if 'BIEM' in reading:
            print("DING!")
            selected = randint(0, len(files)-1)
            print(selected)
            play(audio_file_path + files[selected])


def play(audio_file):
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


thread = threading.Thread(target=read_serial, args=(serial_port,))
thread.start()
