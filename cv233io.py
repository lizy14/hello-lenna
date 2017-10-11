import cv2
import numpy
from PyQt5.QtGui import QPixmap, QImage


LOAD_FILTER = "OpenCV-supported images (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 *.png *.webp *.pbm *.pgm *.ppm *.sr *.ras *.tiff *.tif)"
SAVE_FILTER = "Windows bitmaps (*.bmp *.dib);;JPEG files (*.jpeg *.jpg *.jpe);;JPEG 2000 files (*.jp2);;Portable Network Graphics (*.png);;WebP (*.webp);;Portable image format (*.pbm *.pgm *.ppm);;Sun rasters (*.sr *.ras);;TIFF files (*.tiff *.tif)"


def load(filename):
    return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)


def save(img, filename):
    cv2.imwrite(filename, cv2.cvtColor(numpy.array(img, dtype='uint8'), cv2.COLOR_BGR2RGB))


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
