from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QSizePolicy, QScrollArea, QLayout, QAction, QToolButton
from PyQt5.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt5.QtCore import Qt
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase

KI = Krita.instance()


class CustomPreview(DockWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(Krita.krita_i18n("Custom Preview"))

        self.foregroundImage = QImage()
        self.backgroundImage = QImage()

        mainWidget = QWidget(self)
        layout = QVBoxLayout(mainWidget)

        # preview
        self.scrollArea = QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.previewLabel = QLabel()
        self.previewLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
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

        # scale images
        dim = self.scrollArea.contentsRect()
        previewImage = previewImage.scaled(dim.width(), dim.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
        if not self.foregroundImage.isNull():
            self.foregroundImage = self.foregroundImage.scaled(dim.width(), dim.height(), Qt.KeepAspectRatio, Qt.FastTransformation)
        if not self.backgroundImage.isNull():
            self.backgroundImage = self.backgroundImage.scaled(dim.width(), dim.height(), Qt.KeepAspectRatio, Qt.FastTransformation)

        # merge images
        resultImage = QImage(previewImage.width(), previewImage.height(), QImage.Format_ARGB32_Premultiplied)
        resultImage.fill(0)
        painter = QPainter(resultImage)
        painter.drawImage(0, 0, self.backgroundImage)
        painter.drawImage(0, 0, previewImage)
        painter.drawImage(0, 0, self.foregroundImage)
        painter.end()

        self.previewLabel.setPixmap(QPixmap.fromImage(resultImage))

    def setForeground(self):
        foregroundFile = QFileDialog.getOpenFileName(self, Krita.krita_i18n("Select foreground image"), filter=Krita.krita_i18n("Images (*.png *.xpm *.jpg)"))[0]
        self.foregroundImage.load(foregroundFile)
        self.refresh()
        print("Custom Preview: Foreground set to " + foregroundFile)

    def setBackground(self):
        backgroundFile = QFileDialog.getOpenFileName(self, Krita.krita_i18n("Select background image"), filter=Krita.krita_i18n("Images (*.png *.xpm *.jpg)"))[0]
        self.backgroundImage.load(backgroundFile)
        self.refresh()
        print("Custom Preview: Background set to " + backgroundFile)

    def removeForegroundAndBackground(self):
        self.foregroundImage = QImage()
        self.backgroundImage = QImage()
        self.refresh()
        print("Custom Preview: Foreground and background reset")


KI.addDockWidgetFactory(DockWidgetFactory("customPreview", DockWidgetFactoryBase.DockRight, CustomPreview))

# TODO make docker disabled when no document open
# TODO make scrollArea tight around preview
# TODO fix drawing images of different sizes
# TODO fix clear button
