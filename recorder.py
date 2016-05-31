import numpy as np
from scipy.io.wavfile import write as wrt
import sounddevice as sd
import os
import soundfile as sf
import json,httplib


def parse_upload(fullname,filename):
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/files/'+filename,open(fullname, 'rb').read(), {
        "X-Parse-Application-Id": "lQvCHl3l6NCCO68tEj6L37kQStHNGxDrUX4YmpKU",
        "X-Parse-REST-API-Key": "q2XlWsxSI8GBe5ZjEpygw2Hc2U7WRrthctoAchaM",
        "Content-Type": "File"
        })
        rawreply = connection.getresponse().read()
        result = json.loads(rawreply.decode())
        #print (result)
        connection.request('POST', '/1/classes/BOX1', json.dumps({
        "audio_file": {"name": result['name'],"__type": "File"}}), {
        "X-Parse-Application-Id": "lQvCHl3l6NCCO68tEj6L37kQStHNGxDrUX4YmpKU",
        "X-Parse-REST-API-Key": "q2XlWsxSI8GBe5ZjEpygw2Hc2U7WRrthctoAchaM",
        "Content-Type": "application/json"})
        rawreply2 = connection.getresponse().read()
        results = json.loads(rawreply2.decode())
        #print (results)




class Recorder:
    def __init__(self, fs=44100, duration=1, channel=1):
        self.fs = fs
        self.duration = duration
        self.channels = channel
        self.initialize_sounddevice()

    def initialize_sounddevice(self):
        sd.default.samplerate = self.fs
        sd.default.channels = self.channels

    def save_wav(self, data, file_name):
        #wrt(file_name, self.fs, data)
        sf.write(file_name, data, self.fs)

    def upload_file(self):
        dir = "./audio/"
        #dir2 = "/home/pi/Raspberry_Pi_Recorder/audio_backup/"
        #print ("in upload")
        for fn in os.listdir(dir):
            #if os.path.isfile(fn):
            src = dir + fn
            try:
                parse_upload(src,fn)
                #dest = dir2 +fn
                os.unlink(src)
            except Exception:
                 pass

    
    def record(self):
        my_recording = sd.rec(
                self.duration * self.fs,
                blocking=True,
                dtype='float32')
        return my_recording

    def rms(self, data):
        return 1000 * np.sqrt(np.mean(np.square(data)))
