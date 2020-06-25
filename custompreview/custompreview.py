from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QImage, QPainter, QPixmap
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase, InfoObject
import threading
import time

KI = Krita.instance()


class CustomPreview(DockWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Preview")

        mainWidget = QWidget(self)
        mainWidget.setLayout(QVBoxLayout())
        self.setWidget(mainWidget)

        self.previewLabel = QLabel()
        self.previewLabel.setText("Placeholder")  # TODO remove

        self.layout().addWidget(self.previewLabel)

        # refresh every 2 seconds
        self.startTimer(2000)

    def canvasChanged(self, canvas):
        self.refresh()

    def timerEvent(self, event):
        self.refresh()

    def refresh(self):
        doc = KI.activeDocument()

        # return if no document is open
        if doc is None:
            self.previewLabel.setText("No document open")  # TODO remove
            return

        # get current drawing
        previewImage = doc.projection(0, 0, doc.width(), doc.height())

        # scale it

        # draw it
        self.previewLabel.setPixmap(QPixmap.fromImage(previewImage))


KI.addDockWidgetFactory(DockWidgetFactory("customPreview", DockWidgetFactoryBase.DockRight, CustomPreview))
