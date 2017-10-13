# Hello Lenna

数字媒体(2)<多媒体><图像处理>，44100415，2017秋，陈莉，清华大学软件学院

## Dependencies

* Python 3.6 Interpreter
* opencv-python 3.3
* PyQt 5.9
* Cython and a C Compiler

### Setting up on Windows

* Install [Miniconda with Python 3.6](https://conda.io/miniconda.html), or Anaconda if you like.

* Install [Visual C++ Build Tools 2015](http://landinghub.visualstudio.com/visual-cpp-build-tools), or Visual Studio 2015 if you like. You may skip this step if you don't want to compile yourself.

* Open Anaconda Prompt, goto project directory. Note that the path should not countain any non-ASCII character.

* Install Python dependencies:
    ```
    conda install numpy cython
    pip install opencv-contrib-python pyqt5
    ```

* Compile Cython Source into Python Extension Module (`.pyx` into `.pyd`). You may skip this step if you don't want to compile yourself.
    ```
    python setup.py build_ext --inplace --compiler=msvc
    ```

* All set. Now bring up the main window by running
    ```
    python main.py
    ```

Tested on Windows 10 1703, Python 3.6.1, Anaconda 4.4.0, MSC v.1900, 64-bit (AMD64).

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
Key-in number of degrees, then click button `Rotate`. Alternatively, with the slider, drag to preview and release to finalize.

### Crop recutangularly
Drag with mouse on the image to specify a rectangular area, then click button `Crop Rectangularly`.

