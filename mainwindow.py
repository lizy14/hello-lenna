from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QWidget
from PyQt5.QtCore import pyqtSlot, QRectF, QPointF, QEvent, Qt
from PyQt5.QtGui import QPen, QColor
import PyQt5
import cv233
import cv233io
import numpy


class MyMainWindow(QMainWindow):
    img = None

    crop_rect_graphics_item = None
    crop_start = None
    crop_end = None
    crop_mouse_down = False

    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)

        self.graphicsView.viewport().installEventFilter(self)

        self.progressBar.hide()
        MyMainWindow.showMaximized(self)

        self.img = cv233io.load('lenna.tif')
        self.paint(self.img)
    
    def eventFilter(self, source, event):
        if source is self.graphicsView.viewport():

            if event.type() == QEvent.MouseMove:
                def get_crop_rect(start, end):
                    xmin = min(start.x(), end.x())
                    xmax = max(start.x(), end.x())
                    ymin = min(start.y(), end.y())
                    ymax = max(start.y(), end.y())
                    return QRectF(QPointF(xmin, ymin), QPointF(xmax, ymax))

                if self.crop_mouse_down:
                    pos = self.graphicsView.mapToScene(event.pos())
                    self.crop_end = pos
                    scene = self.graphicsView.scene()
                    scene.removeItem(self.crop_rect_graphics_item)
                    self.crop_rect_graphics_item = scene.addRect(
                        get_crop_rect(self.crop_start, self.crop_end), 
                        QPen(Qt.green, 3, Qt.DashLine, Qt.SquareCap))

            elif event.type() == QEvent.MouseButtonPress:
                self.crop_mouse_down = True
                pos = self.graphicsView.mapToScene(event.pos())
                self.crop_start = pos

            elif event.type() == QEvent.MouseButtonRelease:
                self.crop_mouse_down = False
                pos = self.graphicsView.mapToScene(event.pos())
                if pos == self.crop_start:
                    scene = self.graphicsView.scene()
                    scene.removeItem(self.crop_rect_graphics_item)


        return QWidget.eventFilter(self, source, event)

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