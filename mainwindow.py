from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSlot, QRectF
import cv233

class MyMainWindow(QMainWindow):
    cvImage = None
    cvImageConverted = None
    cvImageRotating = None


    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
    

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


    # slots

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = QFileDialog.getOpenFileName(self)[0]
        if filename:
            self.cvImage = cv233.load(filename)
            self.paint(self.cvImage)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename = QFileDialog.getSaveFileName(self)[0]
        if filename:
            cv233.save(self.cvImage, filename)

    def on_sliderRotation_valueChanged(self, degree):
        self.cvImageRotating = cv233.rotate(self.cvImage, degree)
        self.paint(self.cvImageRotating)

    def on_sliderRotation_sliderReleased(self):
        self.cvImage = self.cvImageRotating

    @pyqtSlot()
    def on_btnClockwise_clicked(self):
        self.cvImage = cv233.transpose(self.cvImage)
        self.cvImage = cv233.flip(self.cvImage, 1)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btnCounterclockwise_clicked(self):
        self.cvImage = cv233.transpose(self.cvImage)
        self.cvImage = cv233.flip(self.cvImage, 0)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btn180_clicked(self):
        self.cvImage = cv233.flip(self.cvImage, -1)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btnVerticalMirror_clicked(self):
        self.cvImage = cv233.flip(self.cvImage, 0)
        self.paint(self.cvImage)
    @pyqtSlot()
    def on_btnHorizontalMirror_clicked(self):
        self.cvImage = cv233.flip(self.cvImage, 1)
        self.paint(self.cvImage)