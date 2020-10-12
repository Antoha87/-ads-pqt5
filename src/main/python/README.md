# Advertisement insertion desktop application

This repository represents structure and way of interface with insertion algorithms

In `main.py` you can find example of data, passed to insertion module and way to interface with it

---
### Instalation
To run this modules successfully you should do following steps:
- Install all listed requirements in *requirements.txt*: 
```
pip install -r requirements.txt
```
- Install [Detectron2](https://github.com/facebookresearch/detectron2/blob/3def12bdeaacd35c6f7b3b6c0097b7bc31f31ba4/INSTALL.md) lib (with CUDA 10.2 preferred)
```
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.6/index.html
```
- Install [ffmpeg](https://ffmpeg.org/download.html) (utility to work with videos) 
```
apt-get install ffmpeg
``` 

**All steps above was tested on Ubuntu 18.04, Python 3.6**

---
#### After `ProcessingExecutor.process_video` call, behavior expected is:
- In `outputs` folder created `report_{video_name}.txt` with data of instances
- `output/instances` folder consist of insertion previews

#### After `InsertionExecutor.insert_ads` call, behavior expected is:
- In `outputs` folder created `{video_name}-processed.mp4` file with result video
- `report_{video_name}.txt` and `output/instances` should be deleted