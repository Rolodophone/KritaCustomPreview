from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QSizePolicy, QScrollArea, QLayout, QAction, QToolButton, QFrame, QStyle
from PyQt5.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt5.QtCore import Qt, QSize, QMargins
from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase

KI = Krita.instance()


class CustomPreview(DockWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(Krita.krita_i18n("Custom Preview"))

        self.foregroundImage = QImage()
        self.backgroundImage = QImage()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # PREVIEW

        self.previewContainer = QWidget()
        layout.addWidget(self.previewContainer)
        self.previewContainer.setContentsMargins(0, 0, 0, 0)
        previewContainerLayout = QHBoxLayout()
        previewContainerLayout.setContentsMargins(0, 0, 0, 0)
        previewContainerLayout.setSpacing(0)
        self.previewContainer.setLayout(previewContainerLayout)
        self.scrollArea = QScrollArea()
        previewContainerLayout.addWidget(self.scrollArea)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.previewLabel = QLabel()
        self.scrollArea.setWidget(self.previewLabel)

        # BUTTONS

        self.buttonLayout = QHBoxLayout()
        layout.addLayout(self.buttonLayout)
        self.buttonLayout.setAlignment(Qt.AlignLeft)

        setForegroundAtn = QAction(self)
        setForegroundAtn.setIconText("Set foreground")
        setForegroundAtn.setIcon(KI.icon("object-order-front-calligra"))
        setForegroundAtn.triggered.connect(self.setForeground)
        setForegroundBtn = QToolButton()
        setForegroundBtn.setDefaultAction(setForegroundAtn)
        self.buttonLayout.addWidget(setForegroundBtn)

        setBackgroundAtn = QAction(self)
        setBackgroundAtn.setIconText(Krita.krita_i18n("Set background"))
        setBackgroundAtn.setIcon(KI.icon("object-order-back-calligra"))
        setBackgroundAtn.triggered.connect(self.setBackground)
        setBackgroundBtn = QToolButton()
        setBackgroundBtn.setDefaultAction(setBackgroundAtn)
        self.buttonLayout.addWidget(setBackgroundBtn)

        removeAtn = QAction(self)
        removeAtn.setIconText(Krita.krita_i18n("Remove foreground and background"))
        removeAtn.setIcon(KI.icon("list-remove"))
        removeAtn.triggered.connect(self.removeForegroundAndBackground)
        removeBtn = QToolButton()
        removeBtn.setDefaultAction(removeAtn)
        self.buttonLayout.addWidget(removeBtn)

        mainWidget = QWidget(self)
        mainWidget.setLayout(layout)
        self.setWidget(mainWidget)

        self.startTimer(500)  # refresh twice a second

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
        dim = self.previewContainer.contentsRect()
        width = dim.width() - self.scrollArea.contentsMargins().top() * 2
        height = dim.height() - self.scrollArea.contentsMargins().top() * 2
        previewImage = previewImage.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
        fgImage = QImage()
        if not self.foregroundImage.isNull():
            fgImage = self.foregroundImage.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
        bgImage = QImage()
        if not self.backgroundImage.isNull():
            bgImage = self.backgroundImage.scaled(width, height, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)

        # merge images
        resultImage = QImage(previewImage.width(), previewImage.height(), QImage.Format_ARGB32_Premultiplied)
        resultImage.fill(0)
        painter = QPainter(resultImage)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawImage(0, 0, bgImage)
        painter.drawImage(0, 0, previewImage)
        painter.drawImage(0, 0, fgImage)
        painter.end()

        self.previewLabel.setPixmap(QPixmap.fromImage(resultImage))

        self.scrollArea.setMaximumSize(previewImage.width() + 4, previewImage.height() + 4)

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


def printSize(size: QSize):
    print(str(size.width()) + ", " + str(size.height()))
