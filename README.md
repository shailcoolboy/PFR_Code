# Raspberry Pi Recorder

## Installation
To download repo use ```git clone https://github.com/aguerrero/Raspberry_Pi_Recorder.git```

Then install all required packages with ```pip install -r requirements.txt```

## Usage
From command line navigate to the directory containing this project and type ```python main.py```

By default recordings will be saved into ```./audio```. This can be changed by changing the values in `./recording.cfg`

## Configuration
The default values are as follows:

    [audio]
    rate 		= 16000
    channels 	= 1
    duration 	= 1
    threshold 	= 1

    [files]
    save_dir = ./audio

Default values can be changed by changing the corresponding values in ```./recording.cfg```