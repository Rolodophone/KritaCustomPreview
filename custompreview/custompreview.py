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
        self.previewLabel.setText("Placeholder")

        self.layout().addWidget(self.previewLabel)

        self.thread = threading.Thread(target=self.threadFun)
        self.thread.start()

    def canvasChanged(self, canvas):
        self.refresh(0)

    def threadFun(self):
        i = 0
        while True:
            time.sleep(5)
            self.refresh(i)
            i += 1

    def refresh(self, i):
        doc = KI.activeDocument()
        self.previewLabel.setText("Document is open")

        # return if no document is open
        if doc is None or doc.isNull():
            self.previewLabel.setText("No document open " + str(i))
            return

        # # get current drawing
        # previewImage = doc.projection()
        #
        # # scale it
        #
        # # draw it
        # self.previewLabel.setPixmap(QPixmap.fromImage(previewImage))
        # self.previewLabel.setText("Changed")
        # self.previewLabel.show()
        # self.previewLabel.update()


KI.addDockWidgetFactory(DockWidgetFactory("customPreview", DockWidgetFactoryBase.DockRight, CustomPreview))
