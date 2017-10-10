from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtCore import pyqtSlot, QRectF
import cv233
import cv233io
import numpy


class MyMainWindow(QMainWindow):
    img = None

    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
        self.progressBar.hide()
        MyMainWindow.showMaximized(self)

        self.img = cv233io.load('lenna.tif')
        self.paint(self.img)

    # I/O helpers

    def paint(self, img):
        pixmap = cv233io.to_QPixmap(img)
        scene = QGraphicsScene(self)
        scene.addPixmap(pixmap)
        scene.setSceneRect(QRectF(pixmap.rect()))
        self.graphicsView.setScene(scene)


    # slots

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = '' or QFileDialog.getOpenFileName(self)[0]
        if filename:
            self.img = cv233io.load(filename)
            self.paint(self.img)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename = QFileDialog.getSaveFileName(self)[0]
        if filename:
            cv233io.save(self.img, filename)

    
    @pyqtSlot()
    def on_btnRotate_clicked(self):
        degree = self.spinBox.value()
        self.img = cv233.rotate(self.img, degree)
        self.paint(self.img)
        
    @pyqtSlot()
    def on_btnClockwise_clicked(self):
        self.img = cv233.transpose(self.img)
        self.img = cv233.horizontal_flip(self.img)
        self.paint(self.img)
    @pyqtSlot()
    def on_btnCounterclockwise_clicked(self):
        self.img = cv233.transpose(self.img)
        self.img = cv233.vertical_flip(self.img)
        self.paint(self.img)
    @pyqtSlot()
    def on_btn180_clicked(self):
        self.img = cv233.horizontal_flip(self.img)
        self.img = cv233.vertical_flip(self.img)
        self.paint(self.img)
    @pyqtSlot()
    def on_btnVerticalMirror_clicked(self):
        self.img = cv233.vertical_flip(self.img)
        self.paint(self.img)
    @pyqtSlot()
    def on_btnHorizontalMirror_clicked(self):
        self.img = cv233.horizontal_flip(self.img)
        self.paint(self.img)