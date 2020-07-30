from PyQt5 import QtCore, QtGui, QtWidgets


class PhotoViewer(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.createActions()

    def setupUi(self, MainWindow, PhotoGallary):
        self.viewer = PhotoGallary

        MainWindow.setObjectName("My Gallary")
        MainWindow.resize(1120, 630)
        # MainWindow.showMaximized()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter.setHandleWidth(10)

        """ LEFT WIDGET """
        self.leftSideWidget = QtWidgets.QWidget(self.splitter)
        self.leftSideWidget.setObjectName("leftSideWidget")
        self.leftSideWidget.setFixedWidth(200)
        self.leftSideWidget.setMinimumWidth(200)
        self.leftSideWidget.setMaximumWidth(300)

        leftWidgetIndex = self.splitter.indexOf(self.leftSideWidget)
        self.splitter.setCollapsible(leftWidgetIndex, False)

        """ LEFT LAYOUT """
        self.leftSideLayout = QtWidgets.QGridLayout(self.leftSideWidget)
        self.leftSideLayout.setContentsMargins(2, 2, 2, 2)
        self.leftSideLayout.setObjectName("leftSideLayout")

        """ RADIO 1 """
        self.file_man = QtWidgets.QRadioButton(self.leftSideWidget)
        self.file_man.setObjectName("file_man")
        self.file_man.setChecked(True)
        self.fileManagerWidgetShow()
        self.leftSideLayout.addWidget(self.file_man, 0, 0, 1, 1)
        """ RADIO 2 """
        self.settings = QtWidgets.QRadioButton(self.leftSideWidget)
        self.settings.setObjectName("settings")
        self.leftSideLayout.addWidget(self.settings, 1, 0, 1, 1)
        """ RADIO 3 """
        self.editPic = QtWidgets.QRadioButton(self.leftSideWidget)
        self.editPic.setObjectName("editPic")
        self.leftSideLayout.addWidget(self.editPic, 2, 0, 1, 1)

        """ MIDDLE WIDGET AND LAYOUT """
        self.middleWidget = QtWidgets.QWidget(self.splitter)
        self.middleWidget.setObjectName("middleWidget")

        middleWidgetIndex = self.splitter.indexOf(self.middleWidget)
        self.splitter.setCollapsible(middleWidgetIndex, False)

        self.middleLayout = QtWidgets.QGridLayout(self.middleWidget)
        self.middleLayout.setContentsMargins(2, 2, 2, 2)
        self.middleLayout.setObjectName("middleLayout")

        """ HORIZONTAL LAYOUT OF BUTTONS --------------------------------------------"""
        self.nextPrevHorizLay = QtWidgets.QHBoxLayout()
        self.nextPrevHorizLay.setObjectName("nextPrevHorizLay")
        """ PREVIOUS BUTTON ---------------------------------------------------------"""
        self.previous = QtWidgets.QPushButton(self.middleWidget)
        self.previous.setFixedWidth(150)
        self.previous.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources\\imgs\\rewind.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous.setIcon(icon)
        self.previous.setObjectName("previous")
        self.nextPrevHorizLay.addWidget(self.previous)
        """ NEXT BUTTON -------------------------------------------------------------"""
        self.next = QtWidgets.QPushButton(self.middleWidget)
        self.next.setFixedWidth(150)
        self.next.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources\\imgs\\fast-forward.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon1)
        self.next.setObjectName("next")
        self.nextPrevHorizLay.addWidget(self.next)

        self.middleLayout.addLayout(self.nextPrevHorizLay, 2, 0, 1, 1)

        self.heading = QtWidgets.QLabel(self.middleWidget)
        self.heading.setObjectName("heading")
        self.heading.setStyleSheet('QLabel#heading {color: green}')
        self.middleLayout.addWidget(self.heading, 0, 0, 1, 1)

        """ THE VIEWER WINDOW """
        self.viewer.setSizeIncrement(QtCore.QSize(0, 0))
        self.viewer.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.viewer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.viewer.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.viewer.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.middleLayout.addWidget(self.viewer, 1, 0, 1, 1)

        """ RIGHT WIDGET AND LAYOUT """
        self.rightSideWidget = QtWidgets.QWidget(self.splitter)
        self.rightSideWidget.setObjectName("rightSideWidget")
        self.rightSideWidget.setFixedWidth(200)
        self.rightSideWidget.setMinimumWidth(200)
        self.rightSideWidget.setMaximumWidth(300)

        rightWidgetIndex = self.splitter.indexOf(self.rightSideWidget)
        self.splitter.setCollapsible(rightWidgetIndex, False)

        self.rightSideLayout = QtWidgets.QGridLayout(self.rightSideWidget)
        self.rightSideLayout.setContentsMargins(0, 0, 0, 0)
        self.rightSideLayout.setObjectName("rightSideLayout")

        """ Face Recog Window """
        self.face_recog = QtWidgets.QRadioButton(self.rightSideWidget)
        self.face_recog.setObjectName("face_recog")
        self.rightSideLayout.addWidget(self.face_recog, 1, 0, 1, 1)

        """ Image Information """
        self.info = QtWidgets.QRadioButton(self.rightSideWidget)
        self.info.setObjectName("info")
        self.info.setChecked(True)

        # self.dynamicImage()
        self.theImageDataWidgetShow()

        self.cameraInfo.setDisabled(True)
        self.gpsInfo.setDisabled(True)
        self.imageOriginInfo.setDisabled(True)
        self.imageInfo.setDisabled(True)

        self.imageInfo.setVisible(True)
        self.gpsInfo.setVisible(True)
        self.imageOriginInfo.setVisible(True)
        self.cameraInfo.setVisible(True)

        self.rightSideLayout.addWidget(self.info, 0, 0, 1, 1)

        self.extra = QtWidgets.QRadioButton(self.rightSideWidget)
        self.extra.setObjectName("extra")
        self.rightSideLayout.addWidget(self.extra, 2, 0, 1, 1)

        # self.infoWidget = QtWidgets.QTableView(self.rightSideWidget)
        # self.infoWidget.setObjectName("infoWidget")
        # self.rightSideLayout.addWidget(self.infoWidget, 3, 0, 1, 1)

        self.mainLayout.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 21))
        self.menubar.setObjectName("menubar")

        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")

        self.viewMenu = QtWidgets.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("helpMenu")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Welcome to Smart Gallary Application")

        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.viewMenu)
        self.menubar.addMenu(self.helpMenu)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    """  ----------------------- The unnamed People to be named ----------------------- """

    def allPeopleWidgetShow(self):
        pass

    def allPeopleWidgetHide(self):
        pass
    """  -------------------------------------------------------------- """

    """  ----------------------- People Data ----------------------- """

    def peopleWidgetShow(self):
        pass

    def peopleWidgetHide(self):
        pass
    """  -------------------------------------------------------------- """

    """  ----------------------- ImageMetaData ----------------------- """

    def theImageDataWidgetShow(self):
        """ -----------------IMAGE METADATA--------------- """
        self.imageInfoLayout = QtWidgets.QVBoxLayout()

        """ Origin """
        self.imageOriginInfo = QtWidgets.QGroupBox("Origin")
        # self.imageOriginInfo = QtWidgets.QGroupBox(self.rightSideWidget)
        # self.imageOriginInfo.setObjectName("Origin")
        layout1 = QtWidgets.QFormLayout()

        self.FileName = QtWidgets.QLineEdit(self.rightSideWidget)
        self.FileName.setObjectName("FileName")
        self.FileName.setReadOnly(True)
        self.FileName.setStyleSheet("QLineEdit#FileName {border: none;}")

        self.FileNameLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.FileNameLabel.setObjectName("FileNameLabel")
        layout1.addRow(self.FileNameLabel, self.FileName)

        self.DateTaken = QtWidgets.QLineEdit(self.rightSideWidget)
        self.DateTaken.setObjectName("DateTaken")
        self.DateTaken.setReadOnly(True)
        self.DateTaken.setStyleSheet("QLineEdit#DateTaken {border: none;}")

        self.DateTakenLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.DateTakenLabel.setObjectName("DateTakenLabel")
        layout1.addRow(self.DateTakenLabel, self.DateTaken)

        self.imageOriginInfo.setLayout(layout1)

        """ GPS """
        self.gpsInfo = QtWidgets.QGroupBox("GPS")
        layout4 = QtWidgets.QFormLayout()

        self.Latitude = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Latitude.setObjectName("Latitude")
        self.Latitude.setReadOnly(True)
        self.Latitude.setStyleSheet("QLineEdit#Latitude {border: none;}")

        self.LatitudeLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.LatitudeLabel.setObjectName("LatitudeLabel")
        layout4.addRow(self.LatitudeLabel, self.Latitude)

        self.Longitude = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Longitude.setObjectName("Longitude")
        self.Longitude.setReadOnly(True)
        self.Longitude.setStyleSheet("QLineEdit#Longitude {border: none;}")

        self.LongitudeLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.LongitudeLabel.setObjectName("LongitudeLabel")
        layout4.addRow(self.LongitudeLabel, self.Longitude)

        self.gpsInfo.setLayout(layout4)

        """ IMAGE DATA """
        self.imageInfo = QtWidgets.QGroupBox("Image")
        layout2 = QtWidgets.QFormLayout()

        self.Dimension = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Dimension.setObjectName("Dimension")
        self.Dimension.setReadOnly(True)
        self.Dimension.setStyleSheet("QLineEdit#Dimension {border: none;}")

        self.DimensionLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.DimensionLabel.setObjectName("DimensionLabel")

        layout2.addRow(self.DimensionLabel, self.Dimension)

        self.Width = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Width.setObjectName("Width")
        self.Width.setReadOnly(True)
        self.Width.setStyleSheet("QLineEdit#Width {border: none;}")

        self.WidthLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.WidthLabel.setObjectName("WidthLabel")

        layout2.addRow(self.WidthLabel, self.Width)

        self.Height = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Height.setObjectName("Height")
        self.Height.setReadOnly(True)
        self.Height.setStyleSheet("QLineEdit#Height {border: none;}")

        self.HeightLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.HeightLabel.setObjectName("HeightLabel")

        layout2.addRow(self.HeightLabel, self.Height)

        self.HResolution = QtWidgets.QLineEdit(self.rightSideWidget)
        self.HResolution.setObjectName("HResolution")
        self.HResolution.setReadOnly(True)
        self.HResolution.setStyleSheet("QLineEdit#HResolution {border: none;}")

        self.HResolutionLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.HResolutionLabel.setObjectName("HResolutionLabel")

        layout2.addRow(self.HResolutionLabel, self.HResolution)

        self.VResolution = QtWidgets.QLineEdit(self.rightSideWidget)
        self.VResolution.setObjectName("VResolution")
        self.VResolution.setReadOnly(True)
        self.VResolution.setStyleSheet("QLineEdit#VResolution {border: none;}")

        self.VResolutionLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.VResolutionLabel.setObjectName("VResolutionLabel")

        layout2.addRow(self.VResolutionLabel, self.VResolution)

        self.BitDepth = QtWidgets.QLineEdit(self.rightSideWidget)
        self.BitDepth.setObjectName("BitDepth")
        self.BitDepth.setReadOnly(True)
        self.BitDepth.setStyleSheet("QLineEdit#BitDepth {border: none;}")

        self.BitDepthLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.BitDepthLabel.setObjectName("BitDepthLabel")

        layout2.addRow(self.BitDepthLabel, self.BitDepth)

        self.imageInfo.setLayout(layout2)

        """ Camera """
        self.cameraInfo = QtWidgets.QGroupBox("Camera")
        layout3 = QtWidgets.QFormLayout()

        self.Maker = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Maker.setObjectName("Maker")
        self.Maker.setReadOnly(True)
        self.Maker.setStyleSheet("QLineEdit#Maker {border: none;}")
        self.MakerLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.MakerLabel.setObjectName("MakerLabel")
        layout3.addRow(self.MakerLabel, self.Maker)

        self.Model = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Model.setObjectName("Model")
        self.Model.setReadOnly(True)
        self.Model.setStyleSheet("QLineEdit#Model {border: none;}")
        self.ModelLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.ModelLabel.setObjectName("ModelLabel")
        layout3.addRow(self.ModelLabel, self.Model)

        self.Fstop = QtWidgets.QLineEdit(self.rightSideWidget)
        self.Fstop.setObjectName("Fstop")
        self.Fstop.setReadOnly(True)
        self.Fstop.setStyleSheet("QLineEdit#Fstop {border: none;}")
        self.FstopLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.FstopLabel.setObjectName("FstopLabel")
        layout3.addRow(self.FstopLabel, self.Fstop)

        self.ExposureTime = QtWidgets.QLineEdit(self.rightSideWidget)
        self.ExposureTime.setObjectName("ExposureTime")
        self.ExposureTime.setReadOnly(True)
        self.ExposureTime.setStyleSheet(
            "QLineEdit#ExposureTime {border: none;}")
        self.ExposureTimeLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.ExposureTimeLabel.setObjectName("ExposureTimeLabel")
        layout3.addRow(self.ExposureTimeLabel, self.ExposureTime)

        self.ISOspeed = QtWidgets.QLineEdit(self.rightSideWidget)
        self.ISOspeed.setObjectName("ISOspeed")
        self.ISOspeed.setReadOnly(True)
        self.ISOspeed.setStyleSheet("QLineEdit#ISOspeed {border: none;}")
        self.ISOspeedLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.ISOspeedLabel.setObjectName("ISOspeedLabel")
        layout3.addRow(self.ISOspeedLabel, self.ISOspeed)

        self.FocalLength = QtWidgets.QLineEdit(self.rightSideWidget)
        self.FocalLength.setObjectName("FocalLength")
        self.FocalLength.setReadOnly(True)
        self.FocalLength.setStyleSheet("QLineEdit#FocalLength {border: none;}")
        self.FocalLengthLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.FocalLengthLabel.setObjectName("FocalLengthLabel")
        layout3.addRow(self.FocalLengthLabel, self.FocalLength)

        self.MeteringMode = QtWidgets.QLineEdit(self.rightSideWidget)
        self.MeteringMode.setObjectName("MeteringMode")
        self.MeteringMode.setReadOnly(True)
        self.MeteringMode.setStyleSheet(
            "QLineEdit#MeteringMode {border: none;}")
        self.MeteringModeLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.MeteringModeLabel.setObjectName("MeteringModeLabel")
        layout3.addRow(self.MeteringModeLabel, self.MeteringMode)

        self.FlashMode = QtWidgets.QLineEdit(self.rightSideWidget)
        self.FlashMode.setObjectName("FlashMode")
        self.FlashMode.setReadOnly(True)
        self.FlashMode.setStyleSheet("QLineEdit#FlashMode {border: none;}")
        self.FlashModeLabel = QtWidgets.QLabel(self.rightSideWidget)
        self.FlashModeLabel.setObjectName("FlashModeLabel")
        layout3.addRow(self.FlashModeLabel, self.FlashMode)

        self.cameraInfo.setLayout(layout3)

        self.imageInfoLayout.addWidget(self.imageOriginInfo)
        self.imageInfoLayout.addWidget(self.imageInfo)
        self.imageInfoLayout.addWidget(self.cameraInfo)
        self.imageInfoLayout.addWidget(self.gpsInfo)
        """ ----------------------------------------------- """
        # self.retranslateUip2()

        self.rightSideLayout.addLayout(self.imageInfoLayout, 3, 0, 1, 1)

    def theImageDataWidgetHide(self):
        self.imageInfo.setVisible(False)
        self.gpsInfo.setVisible(False)
        self.imageOriginInfo.setVisible(False)
        self.cameraInfo.setVisible(False)
    """  -------------------------------------------------------------- """

    """  ----------------------- Edit Photo ----------------------- """
    """ EDIT CROP RESIZE AND CHANGE COLORS """

    def editPhotoWidgetHide(self):
        self.photoGroup.close()

    def editPhotoWidgetShow(self):
        self.editPicLayout = QtWidgets.QVBoxLayout()

        self.photoGroup = QtWidgets.QGroupBox("Edit Image")
        layout = QtWidgets.QFormLayout()
        labelNew = QtWidgets.QLabel("Stay Tuned for the next Update")
        labelNew.setObjectName("labelNew")
        labelNew.setStyleSheet('QLabel#labelNew {color: purple}')
        layout.addRow(labelNew)
        # layout.addRow(QtWidgets.QLabel("Name:"), QtWidgets.QLineEdit())
        # layout.addRow(QtWidgets.QLabel("Crop:"), QtWidgets.QComboBox())
        # layout.addRow(QtWidgets.QLabel("Age:"), QtWidgets.QSpinBox())
        self.photoGroup.setLayout(layout)

        self.editPicLayout.addWidget(self.photoGroup)

        self.leftSideLayout.addLayout(self.editPicLayout, 3, 0, 1, 1)
    """  -------------------------------------------------------------- """

    """  ----------------------- File Manager ----------------------- """

    def fileManagerWidgetHide(self):
        self.enterPath.close()
        self.inputText.close()
        self.backPath.close()
        self.filemanager.close()

    def fileManagerWidgetShow(self):
        self.enterPath = QtWidgets.QLabel(self.leftSideWidget)
        self.enterPath.setObjectName("enterPath")
        self.enterPath.setStyleSheet('QLabel#enterPath {color: black}')
        self.leftSideLayout.addWidget(self.enterPath, 3, 0, 1, 1)
        """ HORIZONRAL LAYOR """
        self.inputPathLay = QtWidgets.QHBoxLayout()
        self.inputPathLay.setObjectName("inputPathLay")
        """ Back Button """
        self.backPath = QtWidgets.QPushButton(self.leftSideWidget)
        self.backPath.setFixedWidth(30)
        self.backPath.setText("")
        iconF = QtGui.QIcon()
        iconF.addPixmap(QtGui.QPixmap("resources\imgs\left-arrow.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backPath.setIcon(iconF)
        self.backPath.setObjectName("backPath")
        self.inputPathLay.addWidget(self.backPath)
        """ INPUT TEXT PATH FOR THE FOLDER """
        self.inputText = QtWidgets.QLineEdit(self.leftSideWidget)
        self.inputText.resize(280, 45)
        self.inputPathLay.addWidget(self.inputText)
        # """ BUTTON TO ENTER THE PATH"""
        # self.pathButton = QtWidgets.QPushButton(self.leftSideWidget)
        # self.pathButton.setFixedWidth(60)
        # self.pathButton.setText("Enter")
        # self.pathButton.setObjectName("path")
        # self.inputPathLay.addWidget(self.pathButton)
        """ ADDING HRLAYOR TO THE LEFT SIDE LAYOR """
        self.leftSideLayout.addLayout(self.inputPathLay, 4, 0, 1, 1)

        self.filemanager = QtWidgets.QTreeView(self.leftSideWidget)
        self.filemanager.setObjectName("filemanager")
        self.filemanager.setSortingEnabled(True)
        self.leftSideLayout.addWidget(self.filemanager, 5, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.enterPath.setText(_translate(
            "MainWindow", "Enter the path of folder"))
    """  -------------------------------------------------------------- """

    """  ----------------------- Application Settings ----------------------- """

    def settingsWidgetHide(self):
        self.formGroupBox.close()

    def settingsWidgetShow(self):
        self.settingsMainLayout = QtWidgets.QVBoxLayout()

        self.formGroupBox = QtWidgets.QGroupBox("Configure Settings")
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Name:"), QtWidgets.QLineEdit())
        layout.addRow(QtWidgets.QLabel("Country:"), QtWidgets.QComboBox())
        layout.addRow(QtWidgets.QLabel("Age:"), QtWidgets.QSpinBox())
        self.formGroupBox.setLayout(layout)

        self.settingsMainLayout.addWidget(self.formGroupBox)

        self.leftSideLayout.addLayout(self.settingsMainLayout, 3, 0, 1, 1)
    """  -------------------------------------------------------------- """

    def contextMenuEvent(self, eventN):
        contextMenu = QtWidgets.QMenu(self)
        fitScreenAction = contextMenu.addAction("Fit to Screen")
        nextAction = contextMenu.addAction("Next Image")
        previousAction = contextMenu.addAction("Previous Image")
        action = contextMenu.exec_(self.mapToGlobal(eventN.pos()))
        if action == fitScreenAction:
            self.viewer.fitInView()
        if action == nextAction:
            self.showImage()
        if action == previousAction:
            self.showImage()

    def createActions(self):
        self.openAct = QtWidgets.QAction(
            "&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QtWidgets.QAction(
            "&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QtWidgets.QAction(
            "E&xit", self, shortcut="Ctrl+Q", triggered=QtCore.QCoreApplication.quit)
        self.zoomInAct = QtWidgets.QAction(
            "Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QtWidgets.QAction(
            "Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QtWidgets.QAction(
            "&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QtWidgets.QAction(
            "&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QtWidgets.QAction(
            "About &Qt", self, triggered=QtWidgets.QApplication.instance().aboutQt)

    def open(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                            QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "Image Viewer",
                                                  "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QtGui.QtPrintSupport.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),
                                size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Gallary"))

        self.file_man.setText(_translate("MainWindow", "File Manager"))
        self.heading.setText(_translate(
            "MainWindow", "Welcome to the Gallary"))
        self.settings.setText(_translate("MainWindow", "Settings"))
        self.editPic.setText(_translate("MainWindow", "Edit Photo"))
        self.info.setText(_translate("MainWindow", "Image Information"))
        self.face_recog.setText(_translate("MainWindow", "Unknown People"))
        self.extra.setText(_translate("MainWindow", "People"))
        self.fileMenu.setTitle(_translate("MainWindow", "File"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))
        self.viewMenu.setTitle(_translate("MainWindow", "View"))
        self.helpMenu.setTitle(_translate("MainWindow", "Help"))
        self.enterPath.setText(_translate(
            "MainWindow", "Enter path of folder"))
        # self.labelNewS.setText(_translate("MainWindow", "Select an Image to explore.. "))
        # def retranslateUip2(self):
        # _translate = QtCore.QCoreApplication.translate
        # self.imageOriginInfo.setTitle(_translate("MainWindow", "Origin"))
        self.FileNameLabel.setText(_translate("MainWindow", "FileName"))
        self.DateTakenLabel.setText(_translate("MainWindow", "DateTaken"))
        # self.gpsInfo.setText(_translate("MainWindow", "GPS"))
        self.LatitudeLabel.setText(_translate("MainWindow", "Latitude"))
        self.LongitudeLabel.setText(_translate("MainWindow", "Longitude"))
        # self.imageInfo.setText(_translate("MainWindow", "Image"))
        self.DimensionLabel.setText(_translate("MainWindow", "Dimension"))
        self.WidthLabel.setText(_translate("MainWindow", "Width"))
        self.HeightLabel.setText(_translate("MainWindow", "Height"))
        self.HResolutionLabel.setText(_translate("MainWindow", "HResolution"))
        self.VResolutionLabel.setText(_translate("MainWindow", "VResolution"))
        self.BitDepthLabel.setText(_translate("MainWindow", "BitDepth"))
        # self.cameraInfo.setText(_translate("MainWindow", "Camera"))
        self.MakerLabel.setText(_translate("MainWindow", "Maker"))
        self.ModelLabel.setText(_translate("MainWindow", "Model"))
        self.FstopLabel.setText(_translate("MainWindow", "Fstop"))
        self.ExposureTimeLabel.setText(
            _translate("MainWindow", "ExposureTime"))
        self.ISOspeedLabel.setText(_translate("MainWindow", "ISOspeed"))
        self.FocalLengthLabel.setText(_translate("MainWindow", "FocalLength"))
        self.MeteringModeLabel.setText(
            _translate("MainWindow", "MeteringMode"))
        self.FlashModeLabel.setText(_translate("MainWindow", "FlashMode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    viewer = PhotoViewer(MainWindow)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, viewer)
    MainWindow.show()
    sys.exit(app.exec_())
