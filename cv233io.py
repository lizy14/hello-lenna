import cv2
import numpy
from PyQt5.QtGui import QPixmap, QImage
import os


LOAD_FILTER = '''\
OpenCV-supported images (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 *.png \
*.webp *.pbm *.pgm *.ppm *.sr *.ras *.tiff *.tif)'''

SAVE_FILTER = '''\
Windows bitmaps (*.bmp *.dib);;\
JPEG files (*.jpeg *.jpg *.jpe);;\
JPEG 2000 files (*.jp2);;\
Portable Network Graphics (*.png);;\
WebP (*.webp);;Portable image format (*.pbm *.pgm *.ppm);;\
Sun rasters (*.sr *.ras);;\
TIFF files (*.tiff *.tif)'''


def load(filename):
    with open(filename, "rb") as f:
        raw_bytes = bytearray(f.read())
    numpyarray = numpy.asarray(raw_bytes, dtype=numpy.uint8)
    img_bgr = cv2.imdecode(numpyarray, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb


def save(img_rgb, filename):
    ext = os.path.splitext(filename)[1]

    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
    numpyarray = cv2.imencode(ext, img_bgr)[1]
    raw_bytes = numpyarray.tobytes()
    with open(filename, 'wb') as f:
        f.write(bytearray(raw_bytes))


def new_img(w, h):
    result = numpy.empty((h, w, 3), dtype='uint8')
    result.fill(255)
    return result


def to_QPixmap(img):
    img = numpy.array(img, dtype='uint8')
    height, width, byteValue = img.shape
    byteValue = byteValue * width
    qImage = QImage(img, width, height, byteValue, QImage.Format_RGB888)
    qPixmap = QPixmap.fromImage(qImage)
    return qPixmap
