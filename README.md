# Hello Lenna

数字媒体(2)<多媒体><图像处理>，44100415，2017秋，陈莉，清华大学软件学院

## Dependencies

* Python 3.6.1
* opencv-contrib-python 3.3.0
* PyQt 5.9.1

### Setting up on Windows

Install [Miniconda with Python 3.6](https://conda.io/miniconda.html).

Open Anaconda Prompt, goto project directory (path should not countain any non-ASCII characters), then run

```
conda install numpy
pip install opencv-contrib-python pyqt5
python main.py
```

Tested on Windows 10.0.15063.

## Assignment 1

### Input / Output
Under menu `Files`.

### Mirror 
* horizontally
* vertically

### Rotate
* 90 degrees clockwise
* 90 degrees counter-clockwise
* 180 degrees

### Rorate arbitray degrees (*)
Key-in number of degrees, then click button `Rotate`.
Note that a rotation on a 512 x 512 image could take ~10 seconds.

### Crop recutangularly
Drag with mouse on the image to specify a rectangular area, then click button `Crop Rectangularly`.

