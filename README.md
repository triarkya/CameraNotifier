# CameraNotifier

### Features

- check video assets of surveillance cameras for specific objects and notify only if any of those objects are found (e.g. person, car, ...)
- get Telegram notification with the video everytime specific objects are found
- all videos will be deleted locally after checking (default but optional)
- assets can be filtered for creation date, so no detection occurs if you don't want to (e.g. skip videos from every saturday)

### Install

`pip install tensorflow==2.4.0`

`pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0`

`pip install imageai --upgrade`

`brew install ffmpeg / apt install ffmpeg`