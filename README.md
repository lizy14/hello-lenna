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

    * If you see `Unable to find vcvarsall.bat`, you may need to manually find `vcvarsall.bat` and run
        ```
        "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x64
        set DISTUTILS_USE_SDK=1
        set MSSdk=1
        ```
    * If you see `LNK1158: cannot run 'rc.exe'`, you may need to make sure you have `rc.exe`. If you did check "Windows SDK" installing Visual C++, try
        ```
        PATH=C:\Program Files (x86)\Windows Kits\8.1\bin\x64;%PATH%
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
Drag the slider, then click `Apply`.

### Crop recutangularly
Drag with mouse on the image to specify a rectangular area, then click button `Crop Rectangularly`.

## Assignment 2

### Color Adjustment

Drag the sliders, then click `Apply`.

* hue
* saturation
* lightness

### Color Halftone

Drag the slider, then click `Apply`.
