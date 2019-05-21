# MHP_Raspicam

This repo contains code used to run the Monash Human Power camera system. It is write protected to ensure it is always left in a working state.

## Important-changes log
  - Added `requirements.txt` to work with virtualenv
  - Code for V1.5 is in `Legacy` folder, code for V2 is in `CameraOverlay`

## Dependencies
To install Pillow (PIL fork), RPi.GPIO, paho-mqtt on Raspberry Pi: **haven't tested on fresh Raspberry Pi**
  - install virtual env `sudo pip3 install virualenv`
  - install system dependencies listed in Pillow's [doc](https://pillow.readthedocs.io/en/latest/installation.html#linux-installation) `sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev`
  - in MHP_Raspicam folder, run 
    ```
    virtualenv venv
    source venv/bin/activate   
    ````
  - install python dependencies `pip3 install -r requirements.txt` **haven't tested**
  - PROFIT!
