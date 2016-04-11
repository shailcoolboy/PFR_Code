import configparser
import os
import recorder
import sys
import time
import numpy as np
import netifaces as ni



def get_config(config_file='recording.cfg'):
    full_path = os.path.join(os.getcwd(), config_file)
    if not os.path.exists(full_path):
        print("{} does not exist".format(config_file))
        sys.exit(1)
    else:
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        return cfg

def setup_save_dir(cfg):
    try:
        full_path = cfg['files']['save_dir']
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        return full_path
    except KeyError:
        sys.exit(1)

def get_sampling_rate(cfg):
    try:
        return int(cfg['audio']['rate'])
    except KeyError:
        sys.exit(1)

def get_channels(cfg):
    try:
        return int(cfg['audio']['channels'])
    except KeyError:
        sys.exit(1)

def get_duration(cfg):
    try:
        return int(cfg['audio']['duration'])
    except KeyError:
        sys.exit(1)

def get_threshold(cfg):
    try:
        return int(cfg['audio']['threshold'])
    except KeyError:
        sys.exit(1)

def process_recording(recorder, recording, threshold, save_dir):
    print recorder.rms(recording)
    if recorder.rms(recording) > threshold:
        timestamp = os.path.join(save_dir, time.strftime("%Y%b%d-%H_%M_%S")+'.wav')
        recorder.save_wav(recording, timestamp)
        recorder.upload_file()

def main():
    cfg = get_config()
    save_dir = setup_save_dir(cfg)
    threshold = get_threshold(cfg)
    fs = get_sampling_rate(cfg)
    duration = get_duration(cfg)
    channels = get_channels(cfg)
    r = recorder.Recorder(fs, duration, channels)

    while True:
        recording = r.record()
        process_recording(r, recording, threshold, save_dir)

if __name__ == '__main__':
    main()
