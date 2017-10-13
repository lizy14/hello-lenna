from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QWidget, QApplication
from PyQt5.QtCore import pyqtSlot, QRectF, QPointF, QEvent, Qt
from PyQt5.QtGui import QPen, QColor
import PyQt5
import pyximport; pyximport.install()
import cv233cpp as cv233
import cv233io
import numpy


class MyMainWindow(QMainWindow):
    img = None
    imgRotating = None

    crop_rect_graphics_item = None
    crop_rect = None
    crop_start = None
    crop_end = None
    crop_mouse_down = False
    
    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)

        self.graphicsView.viewport().installEventFilter(self)

        self.progressBar.hide()
        MyMainWindow.showMaximized(self)
        try:
            self.img = cv233io.load('lenna.tif')
            self.paint(self.img)
        except:
            pass
    
    def eventFilter(self, source, event):
        if source is self.graphicsView.viewport() and self.graphicsView.scene() is not None:

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
                    self.crop_rect = get_crop_rect(self.crop_start, self.crop_end)

                    scene = self.graphicsView.scene()
                    scene.removeItem(self.crop_rect_graphics_item)
                    self.crop_rect_graphics_item = scene.addRect(
                        self.crop_rect, 
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
        rect = QRectF(pixmap.rect())
        scene.addRect(rect, QPen(Qt.black, 3, Qt.SolidLine, Qt.SquareCap))
        scene.setSceneRect(rect)
        self.graphicsView.setScene(scene)


    # slots

    def on_sliderRotation_valueChanged(self, degree):
        self.imgRotating = cv233.rotate(self.img, degree)
        self.paint(self.imgRotating)

    def on_sliderRotation_sliderReleased(self):
        self.img = self.imgRotating

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = '' or QFileDialog.getOpenFileName(self, filter=cv233io.LOAD_FILTER)[0]
        if filename:
            self.img = cv233io.load(filename)
            self.paint(self.img)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename = QFileDialog.getSaveFileName(self, filter=cv233io.SAVE_FILTER)[0]
        if filename:
            cv233io.save(self.img, filename)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        QApplication.quit()
    
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

    @pyqtSlot()
    def on_btnCrop_clicked(self):

        rect = self.crop_rect
        if rect is None:
            return
        self.crop_rect = None

        self.img = cv233.crop(self.img, 
            int(rect.topLeft().x()), 
            int(rect.bottomRight().x()), 
            int(rect.topLeft().y()), 
            int(rect.bottomRight().y()))
        self.paint(self.img)