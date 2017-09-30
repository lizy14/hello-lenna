import cv2
import numpy
from PyQt5.QtGui import QPixmap, QImage


def load(filename):
    return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB).tolist()


def save(img, filename):
    cv2.imwrite(filename, cv2.cvtColor(numpy.array(img, dtype='uint8'), cv2.COLOR_BGR2RGB))


def to_QPixmap(img):
    img = numpy.array(img, dtype='uint8')
    height, width, byteValue = img.shape
    byteValue = byteValue * width
    qImage = QImage(img, width, height, byteValue, QImage.Format_RGB888)
    qPixmap = QPixmap.fromImage(qImage)
    return qPixmap
