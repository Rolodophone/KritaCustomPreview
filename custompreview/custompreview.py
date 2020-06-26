from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSizePolicy, QScrollArea
from PyQt5.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt5.QtCore import Qt
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase

KI = Krita.instance()


class CustomPreview(DockWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Preview")

        mainWidget = QWidget(self)
        layout = QVBoxLayout(mainWidget)

        # preview
        scrollArea = QScrollArea()
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        self.previewLabel = QLabel()
        self.previewLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        scrollArea.setWidget(self.previewLabel)

        layout.addWidget(scrollArea)

        mainWidget.setLayout(layout)
        self.setWidget(mainWidget)

        # refresh every second
        self.startTimer(1000)

    def canvasChanged(self, canvas):
        self.refresh()

    def timerEvent(self, event):
        self.refresh()

    def resizeEvent(self, event):
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
        dockerDim = self.contentsRect()
        previewImage = previewImage.scaled(dockerDim.width() - 2, dockerDim.height() - 2, Qt.KeepAspectRatio, Qt.FastTransformation)

        # draw it
        self.previewLabel.setPixmap(QPixmap.fromImage(previewImage))


KI.addDockWidgetFactory(DockWidgetFactory("customPreview", DockWidgetFactoryBase.DockRight, CustomPreview))
