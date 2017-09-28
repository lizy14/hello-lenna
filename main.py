import sys
import cv2
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QRectF


class MyMainWindow(QMainWindow):
    cvImage = None
    cvImageConverted = None
    cvImageRotating = None


    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
    
        
    # transformations
    def rotate(self, img, degree):
        rows, cols, _ = img.shape
        M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
        return cv2.warpAffine(img, M, (cols, rows))

    def flip(self, img, direction):
        cv2.flip(img, direction, img)
        return img
    

    # I/O helpers

    def cvImage_to_QPixmap(self, cvImage):
        height, width, byteValue = cvImage.shape
        byteValue = byteValue * width
        qImage = QImage(cvImage, width, height, byteValue, QImage.Format_RGB888)
        qImage = qImage.rgbSwapped() # RGB to BGR
        qPixmap = QPixmap.fromImage(qImage)
        return qPixmap


    def paint(self, cvImage):
        pixmap = self.cvImage_to_QPixmap(cvImage)

        scene = QGraphicsScene(self)
        scene.addPixmap(pixmap)
        scene.setSceneRect(QRectF(pixmap.rect()))
        self.graphicsView.setScene(scene)

            
    def load(self, filename):
        return cv2.imread(filename)


    def save(self, cvImage, filename):
        cv2.imwrite(filename, cvImage)


    # slots

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self)[0]
        if filename:
            self.cvImage = self.load(filename)
            self.paint(self.cvImage)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename = QFileDialog.getSaveFileName(self)[0]
        if filename:
            self.save(self.cvImage, filename)

    def on_sliderRotation_valueChanged(self, degree):
        self.cvImageRotating = self.rotate(self.cvImage, degree)
        self.paint(self.cvImageRotating)
    def on_sliderRotation_sliderReleased(self):
        self.cvImage = self.cvImageRotating

    def rotate_immediately_then_paint(self, degree):
        self.cvImage = self.rotate(self.cvImage, degree)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btnClockwise_clicked(self):
        self.rotate_immediately_then_paint(270)
    @pyqtSlot()
    def on_btnCounterclockwise_clicked(self):
        self.rotate_immediately_then_paint(90)
    @pyqtSlot()
    def on_btn180_clicked(self):
        self.rotate_immediately_then_paint(180)

    def flip_then_paint(self, direction):
        self.cvImage = self.flip(self.cvImage, direction)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btnVerticalMirror_clicked(self):
        self.flip_then_paint(0)
    @pyqtSlot()
    def on_btnHorizontalMirror_clicked(self):
        self.flip_then_paint(1)


def main():
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()