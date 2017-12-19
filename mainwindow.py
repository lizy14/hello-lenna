from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QWidget, QGraphicsItem, QGraphicsEllipseItem, QMessageBox
from PyQt5.QtCore import pyqtSlot, QRectF, QPointF, QEvent, Qt
from PyQt5.QtGui import QPen, QPainterPath, QBrush

import pyximport; import numpy; pyximport.install(setup_args={'include_dirs': numpy.get_include()})

import cv233io
from assignment1 import *
from assignment2 import *
from assignment3 import *
from assignment4 import *
from assignment5 import *
import numpy as np

class MyMainWindow(QMainWindow):
    img = None
    imgRotating = None
    imgColorChanging = None
    imgColorHalftone = None
    imgFreqFilter = None

    crop_rect_graphics_item = None
    crop_rect = None
    crop_start = None
    crop_end = None
    crop_mouse_down = False

    grayscaleMapping = np.arange(256)
    grayscaleTransforming = None
    mappingPathItem = None

    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
        self.connect_signals()
        self.graphicsView.viewport().installEventFilter(self)
        self.mappingView.viewport().installEventFilter(self)

        self.showMaximized()


    def showEvent(self, ev):
        try:
            self.img = cv233io.load('lenna.tif')
            self.paint(self.img)            
        except FileNotFoundError:
            pass

        return QMainWindow.showEvent(self, ev)
        

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
                    self.crop_rect = get_crop_rect(
                        self.crop_start, self.crop_end)

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

        elif source is self.mappingView.viewport() and self.mappingView.scene() is not None:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
                p = self.mappingView.mapToScene(event.pos())
                r = 5
                item = self.mappingView.scene().addEllipse(-r, -r, 2 * r, 2 * r, brush=QBrush(Qt.red))
                item.setPos(p)
                item.setFlag(QGraphicsItem.ItemIsMovable)
                self.updateMapping()
            
        
        return QWidget.eventFilter(self, source, event)

    # I/O helpers

    def paint(self, img):
        pixmap = cv233io.to_QPixmap(img)
        scene = QGraphicsScene(self)
        scene.addPixmap(pixmap)
        rect = QRectF(pixmap.rect())
        if img is self.img:
            scene.addRect(rect, QPen(Qt.black, 3, Qt.SolidLine, Qt.SquareCap))
        else:
            scene.addRect(rect, QPen(Qt.red, 3, Qt.DashLine, Qt.SquareCap))
        scene.setSceneRect(rect)
        self.graphicsView.setScene(scene)
        self.paintHist(img)

    def paintHist(self, img):
        if self.toolBox.currentIndex() == 2: # hist widget visible
            total = img.shape[0] * img.shape[1]
            hist = histogram(img, channel=-1)

            histscene = QGraphicsScene(self)
            tallest = max(hist)
            for i in range(256):
                histscene.addLine(i, tallest, i, tallest - hist[i])
            histscene.setSceneRect(0, 0, 256, tallest)
            self.histView.setScene(histscene)
            def autoScaleView(view):
                rect = view.scene().sceneRect()
                view.fitInView(rect)
            autoScaleView(self.histView)

    # slots
    def connect_signals(self):
        self.sliderH.valueChanged.connect(self.change_hsv)
        self.sliderS.valueChanged.connect(self.change_hsv)
        self.sliderV.valueChanged.connect(self.change_hsv)
        self.comboFreqDirection.currentTextChanged.connect(self.updateFreqFilter)
        self.comboFreqFilter.currentTextChanged.connect(self.updateFreqFilter)
        self.sliderFreqParam.valueChanged.connect(self.updateFreqFilter)
        self.actionExit.triggered.connect(self.close)

    @pyqtSlot(int)
    def on_sliderRotation_valueChanged(self, degree):
        if degree == 0:
            self.paint(self.img)
        else:
            self.imgRotating = rotate(self.img, degree)
            self.paint(self.imgRotating)

    @pyqtSlot()
    def change_hsv(self):
        imgHsv = convertRgbToHsv(self.img)
        self.imgColorChanging = changeHsv(
            imgHsv,
            self.sliderH.value() / 360,
            self.sliderS.value() / 100,
            self.sliderV.value() / 100)
        self.imgColorChanging = convertHsvToRgb(self.imgColorChanging)
        self.paint(self.imgColorChanging)

    @pyqtSlot()
    def on_btnColorApply_clicked(self):
        self.img = self.imgColorChanging
        self.sliderH.setValue(0)
        self.sliderS.setValue(0)
        self.sliderV.setValue(0)
        self.paint(self.img)

    @pyqtSlot(int)
    def on_toolBox_currentChanged(self, index):
        self.paintHist(self.img)
        self.updateMapping()

    @pyqtSlot(int)
    def on_sliderHalftoneSpacing_valueChanged(self, spacing):
        if spacing >= 4:
            self.imgColorHalftone = colorHalftone(self.img, spacing)
            self.paint(self.imgColorHalftone)
        else:
            self.paint(self.img)

    @pyqtSlot()
    def on_btnColorHalftone_clicked(self):
        self.img = self.imgColorHalftone
        self.paint(self.img)

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filename = cv233io.get_filename_to_load(self)
        if filename:
            self.img = cv233io.load(filename)
            self.paint(self.img)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename = cv233io.get_filename_to_save()
        if filename:
            cv233io.save(self.img, filename)

    @pyqtSlot()
    def on_btnRotate_clicked(self):
        self.img = self.imgRotating
        self.sliderRotation.setValue(0) # should trigger self.paint(self.img)

    @pyqtSlot()
    def on_btnClockwise_clicked(self):
        self.img = transpose(self.img)
        self.img = horizontal_flip(self.img)
        self.paint(self.img)

    @pyqtSlot()
    def on_btnCounterclockwise_clicked(self):
        self.img = transpose(self.img)
        self.img = vertical_flip(self.img)
        self.paint(self.img)

    @pyqtSlot()
    def on_btn180_clicked(self):
        self.img = horizontal_flip(self.img)
        self.img = vertical_flip(self.img)
        self.paint(self.img)

    @pyqtSlot()
    def on_btnVerticalMirror_clicked(self):
        self.img = vertical_flip(self.img)
        self.paint(self.img)

    @pyqtSlot()
    def on_btnHorizontalMirror_clicked(self):
        self.img = horizontal_flip(self.img)
        self.paint(self.img)

    def crop(self, circular=False):
        rect = self.crop_rect
        if rect is None:
            return
        self.crop_rect = None

        self.img = crop(
            self.img,
            int(rect.topLeft().x()),
            int(rect.bottomRight().x()),
            int(rect.topLeft().y()),
            int(rect.bottomRight().y()),
            1 if circular else 0)
        self.paint(self.img)

    @pyqtSlot()
    def on_btnCropRect_clicked(self):
        self.crop(circular=False)

    @pyqtSlot()
    def on_btnCropCirc_clicked(self):
        self.crop(circular=True)

    @pyqtSlot(int)
    def on_sliderSvd_valueChanged(self, _):
        upper = min(self.img.shape[:2])
        value = 2 ** self.sliderSvd.value()
        # [1, 512] maps to [1, upper]
        k = (upper - 1) / 511
        b = 1 - k
        depth = int(k * value + b)
        self.paint(svdCompression(self.img, depth))

    @pyqtSlot()
    def on_btnHistEqual_clicked(self):
        self.img = histogramEqualization(self.img)
        self.paint(self.img)

    def resetMappingScene(self):
        mappingscene = QGraphicsScene(self)
        mappingscene.setSceneRect(0, 0, 256, 256)
        mappingscene.changed.connect(self.updateMapping)
        self.mappingView.setScene(mappingscene)
        def autoScaleView(view):
            rect = view.scene().sceneRect()
            view.fitInView(rect)
        autoScaleView(self.mappingView)

    @pyqtSlot()
    def on_btnResetGrayscale_clicked(self):
        self.resetMappingScene()
        self.updateMapping()

    cached_keypoints = None
    cached_method = None
    def updateMapping(self):
        if self.toolBox.currentIndex() == 2: # widget visible

            if self.mappingView.scene() is None:
                self.resetMappingScene()
            
            mappingscene = self.mappingView.scene()

            keypoints = [item.scenePos() for item in mappingscene.items() if isinstance(item, QGraphicsEllipseItem)]
            keypoints.sort(key=lambda p: p.x())
            
            method = self.comboGrayscale.currentText()
            if method == self.cached_method and keypoints == self.cached_keypoints:
                return
            self.cached_keypoints = keypoints
            self.cached_method = method

            # update grayscaleMapping
            try:
                if method == 'Linear':
                    keypoints = [[p.x(), 256 - p.y()]for p in keypoints]
                    keypoints.insert(0, [0, 0])
                    keypoints.append([255, 255])
                    self.grayscaleMapping = np.interp(
                        np.arange(256), 
                        [p[0] for p in keypoints],
                        [p[1] for p in keypoints])
                else:
                    self.grayscaleMapping = np.arange(256)
                    # log, exp, gamma need exactly one point
                    if len(keypoints) != 1:
                        pass
                    else:
                        p = keypoints[0]
                        x0 = p.x()
                        y0 = 256 - p.y()
                        if method == 'Logarithmic':
                            pass
                        elif method == 'Exponential':
                            pass
                        elif method == 'Gamma':
                            gamma = np.log(y0 / 256) / np.log(x0 / 256)
                            self.grayscaleMapping = 256 * (self.grayscaleMapping / 256) ** gamma
            except Exception:
               self.grayscaleMapping = np.arange(256)

            path = QPainterPath()
            for i in range(0, 256):
                if i == 0:
                    path.moveTo(0, 255 - self.grayscaleMapping[0])
                else:
                    path.lineTo(i, 255 - self.grayscaleMapping[i])
            
            if self.mappingPathItem is not None:
                mappingscene.removeItem(self.mappingPathItem)
            self.mappingPathItem = mappingscene.addPath(path)

            self.grayscaleTransforming = grayscaleTransformation(self.img, self.grayscaleMapping)
            self.paint(self.grayscaleTransforming)



        
    @pyqtSlot()
    def on_btnApplyGrayscale_clicked(self):
        if self.grayscaleTransforming is not None:
            self.img = self.grayscaleTransforming
        self.paint(self.img)


    @pyqtSlot(str)
    def on_comboGrayscale_currentTextChanged(self, _):
        self.updateMapping()

    @pyqtSlot()
    def on_btnMedFilt_clicked(self):
        kernel_size = self.sliderMedFilt.value()
        if kernel_size % 2 != 1 or kernel_size < 0:
            QMessageBox.critical(self, "Bad kernel size", "Kernel size expected to be an odd positive integer.")
        self.img = medianFilter(self.img, kernel_size)
        self.paint(self.img)
    
    @pyqtSlot()
    def on_btnGaussianFilter_clicked(self):
        sigma = self.sliderGaussianFilterSigma.value()
        self.img = gaussianFilter(self.img, sigma)
        self.paint(self.img)
        
    @pyqtSlot()
    def on_btnSharpen_clicked(self):
        self.img = sharpen(self.img)
        self.paint(self.img)

    @pyqtSlot()
    def on_btnSnow_clicked(self):
        self.img = snow(self.img)
        self.paint(self.img)
    
    @pyqtSlot()        
    def updateFreqFilter(self):
        method = self.comboFreqFilter.currentText()
        param = self.sliderFreqParam.value()
        direction = self.comboFreqDirection.currentText()
        if direction == 'Blur':
            operator = freqBlur
        elif direction == 'Sharpen':
            operator = lambda *args, **kwargs: histogramEqualization(freqSharpen(*args, **kwargs))
        else:
            raise AssertionError('direction neither Blur nor Sharpen')
        param = int(2. ** (9. - param / 10.))
        self.imgFreqFilter = operator(self.img, method, param)
        self.paint(self.imgFreqFilter)

    @pyqtSlot()
    def on_btnFreqFilter_clicked(self):
        self.img = self.imgFreqFilter
        self.paint(self.img)