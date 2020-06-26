from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QSizePolicy, QScrollArea, QLayout, QAction, QToolButton
from PyQt5.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt5.QtCore import Qt
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase

KI = Krita.instance()


class CustomPreview(DockWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(Krita.krita_i18n("Custom Preview"))

        mainWidget = QWidget(self)
        layout = QVBoxLayout(mainWidget)

        # preview
        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.previewLabel = QLabel()
        self.previewLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scrollArea.setWidget(self.previewLabel)

        # BUTTONS

        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignLeft)

        setForegroundAtn = QAction(self)
        setForegroundAtn.setIconText("Set foreground")
        setForegroundAtn.setIcon(KI.icon("object-order-front-calligra"))
        setForegroundAtn.triggered.connect(self.setForeground)
        setForegroundBtn = QToolButton()
        setForegroundBtn.setDefaultAction(setForegroundAtn)
        buttonLayout.addWidget(setForegroundBtn)

        setBackgroundAtn = QAction(self)
        setBackgroundAtn.setIconText(Krita.krita_i18n("Set background"))
        setBackgroundAtn.setIcon(KI.icon("object-order-back-calligra"))
        setBackgroundAtn.triggered.connect(self.setBackground)
        setBackgroundBtn = QToolButton()
        setBackgroundBtn.setDefaultAction(setBackgroundAtn)
        buttonLayout.addWidget(setBackgroundBtn)

        removeAtn = QAction(self)
        removeAtn.setIconText(Krita.krita_i18n("Remove foreground and background"))
        removeAtn.setIcon(KI.icon("list-remove"))
        removeAtn.triggered.connect(self.removeForegroundAndBackground)
        removeBtn = QToolButton()
        removeBtn.setDefaultAction(removeAtn)
        buttonLayout.addWidget(removeBtn)

        # adding widgets to layout
        layout.addWidget(self.scrollArea)
        layout.addLayout(buttonLayout)

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
            return

        # get current drawing
        previewImage = doc.projection(0, 0, doc.width(), doc.height())

        # scale it
        dockerDim = self.scrollArea.contentsRect()
        previewImage = previewImage.scaled(dockerDim.width(), dockerDim.height(), Qt.KeepAspectRatio, Qt.FastTransformation)

        # draw it
        self.previewLabel.setPixmap(QPixmap.fromImage(previewImage))

    def setForeground(self):
        pass

    def setBackground(self):
        pass

    def removeForegroundAndBackground(self):
        pass


KI.addDockWidgetFactory(DockWidgetFactory("customPreview", DockWidgetFactoryBase.DockRight, CustomPreview))
