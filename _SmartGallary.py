import glob
import os
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from faceD import RecogFaces
from _design import Ui_MainWindow, PhotoViewer
from _metadata import ImageMetaData


class Gallary(QtWidgets.QMainWindow):
    def __init__(self, MainWindow):
        super(Gallary, self).__init__()

        self.viewer = PhotoViewer(MainWindow)
        self.windowNew = Ui_MainWindow()
        self.metadata = ImageMetaData()

        self.windowNew.setupUi(MainWindow, self.viewer)
        # MainWindow.setStyleSheet("background-color : rgba(30, 30, 30, 255); color: white;")

        self.facerec = RecogFaces()

        self.classifier = None
        self.predictions = None
        self.filesTestNameList = []
        self.image_path = ""
        self.fileSelected = ""
        self.model_saved_on_path = ""
        self.folderName = ""
        self.folderTrainName = ""
        self.folderTestName = ""
        self.theFolderPath = None
        self.theCurrentWorkingPath = os.getcwd()
        print(self.theCurrentWorkingPath)

        self.initUI()
        MainWindow.show()

    def initUI(self):
        self.windowNew.previous.clicked.connect(self.previousImage)
        self.windowNew.next.clicked.connect(self.nextImage)
        self.windowNew.file_man.toggled.connect(
            lambda: self.checkRadioLeft(self.windowNew.file_man))
        self.windowNew.settings.toggled.connect(
            lambda: self.checkRadioLeft(self.windowNew.settings))
        self.windowNew.editPic.toggled.connect(
            lambda: self.checkRadioLeft(self.windowNew.editPic))

        self.windowNew.info.toggled.connect(
            lambda: self.checkRadioRight(self.windowNew.info))
        # self.windowNew.info.toggled.connect(lambda:self.checkRadioRight(self.windowNew.info))
        # self.windowNew.info.toggled.connect(lambda:self.checkRadioRight(self.windowNew.info))

        # self.windowNew.inputText = QtWidgets.QLineEdit()
        # self.windowNew.backPath = QtWidgets.QPushButton()
        self.windowNew.inputText.returnPressed.connect(self.onChangedPath)
        self.windowNew.backPath.clicked.connect(self.backBPressed)
        # self.windowNew.pathButton.clicked.connect(self.changePathFindFolder)

    def previousImage(self):
        if self.fileSelected is not None:
            relevant_path = os.path.dirname(self.fileSelected)
            included_extensions = ['jpg', 'JPG', 'JPEG',
                                   'PNG', 'jpeg', 'bmp', 'png', 'gif']
            fileList = [fn for fn in os.listdir(relevant_path)
                        if any(fn.endswith(ext) for ext in included_extensions)]
            theFileName = os.path.basename(self.fileSelected)
            # print(fileList, theFileName)
            try:
                prevIndex = fileList.index(theFileName) - 1
                # print(prevIndex, fileList.index(theFileName))
                if prevIndex < 0 or prevIndex == len(fileList):
                    pass
                else:
                    thePrevImage = str(relevant_path)+"/"+fileList[prevIndex]
                    # print(thePrevImage)
                    trans = QtCore.QCoreApplication.translate
                    self.windowNew.heading.setText(
                        trans("MainWindow", str(fileList[prevIndex])))
                    self.fileSelected = thePrevImage
                    self.showMetaDataInInfoTab(str(fileList[prevIndex]), trans)
                    self.showImage(self.fileSelected)
            except ValueError:
                pass
        else:
            print("Don't click previous without selecting an Image.. ")

    def nextImage(self):
        if self.fileSelected is not None:
            relevant_path = os.path.dirname(self.fileSelected)
            included_extensions = ['jpg', 'JPG', 'JPEG',
                                   'PNG', 'jpeg', 'bmp', 'png', 'gif']
            fileList = [fn for fn in os.listdir(relevant_path)
                        if any(fn.endswith(ext) for ext in included_extensions)]
            theFileName = os.path.basename(self.fileSelected)
            # print(fileList, theFileName)
            try:
                nextIndex = fileList.index(theFileName) + 1
                # print(nextIndex, fileList.index(theFileName))
                if nextIndex < 0 or nextIndex == len(fileList):
                    pass
                else:
                    theNextImage = str(relevant_path)+"/"+fileList[nextIndex]
                    # print(theNextImage)
                    trans = QtCore.QCoreApplication.translate
                    self.windowNew.heading.setText(
                        trans("MainWindow", str(fileList[nextIndex])))
                    self.fileSelected = theNextImage
                    self.showMetaDataInInfoTab(str(fileList[nextIndex]), trans)
                    self.showImage(self.fileSelected)
            except ValueError:
                pass
        else:
            print("Don't click next without selecting an Image.. ")

    def checkRadioLeft(self, buttonState):
        if buttonState.text() == "File Manager":
            if buttonState.isChecked() == True:
                # print (buttonState.text(), " is selected")
                self.windowNew.fileManagerWidgetShow()
                if self.theFolderPath is not None:
                    # relevant_path = os.path.dirname(self.fileSelected)
                    self.changePathFindFolder(self.theFolderPath)
                    self.windowNew.inputText.setText(str(self.theFolderPath))
                self.windowNew.inputText.returnPressed.connect(
                    self.onChangedPath)
                self.windowNew.backPath.clicked.connect(self.backBPressed)
            else:
                # print (buttonState.text(), " is deselected")
                self.windowNew.fileManagerWidgetHide()

        if buttonState.text() == "Settings":
            if buttonState.isChecked() == True:
                # print (buttonState.text(), " is selected")
                self.windowNew.settingsWidgetShow()
            else:
                # print (buttonState.text(), " is deselected")
                self.windowNew.settingsWidgetHide()

        if buttonState.text() == "Edit Photo":
            if buttonState.isChecked() == True:
                # print (buttonState.text(), " is selected")
                self.windowNew.editPhotoWidgetShow()
            else:
                # print (buttonState.text(), " is deselected")
                self.windowNew.editPhotoWidgetHide()

    def checkRadioRight(self, buttonState):
        if buttonState.text() == "Image Information":
            if buttonState.isChecked() == True:
                print(buttonState.text(), " is selected")
                # self.windowNew.theImageDataWidgetShow()
                self.windowNew.imageInfo.setVisible(True)
                self.windowNew.gpsInfo.setVisible(True)
                self.windowNew.imageOriginInfo.setVisible(True)
                self.windowNew.cameraInfo.setVisible(True)
            else:
                print(buttonState.text(), " is deselected")
                self.windowNew.theImageDataWidgetHide()

        # if buttonState.text() == "Image Information":
        #     if buttonState.isChecked() == True:
        #         print (buttonState.text(), " is selected")
        #     else:
        #         print (buttonState.text(), " is deselected")
        #         self.windowNew.theImageDataWidgetHide()
        #         self.windowNew.imageInfoGrpHide()

    def onChangedPath(self):
        self.textboxPath = self.windowNew.inputText.text()
        self.changePathFindFolder(self.textboxPath)
        self.windowNew.inputText.setText(str(self.textboxPath))
        self.theCurrentWorkingPath = self.textboxPath

    def backBPressed(self):
        if self.theCurrentWorkingPath:
            newPath = os.path.dirname(self.theCurrentWorkingPath)
            self.changePathFindFolder(newPath)
            self.windowNew.inputText.setText(str(newPath))
            self.theCurrentWorkingPath = newPath
        else:
            # Set statusbar choose path first
            pass

    def changePathFindFolder(self, thePath):
        # self.textboxValue = self.windowNew.inputText.text()
        # QtWidgets.QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        # self.windowNew.inputText.setText("")

        path = str(thePath)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        filters = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"]
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        self.model.setReadOnly(True)

        self.indexRoot = self.model.index(path)

        self.windowNew.filemanager.setModel(self.model)
        self.windowNew.filemanager.setRootIndex(self.indexRoot)
        self.windowNew.filemanager.clicked.connect(self.on_treeView_clicked)
        self.windowNew.filemanager.doubleClicked.connect(
            self.on_treeView_doubleClicked)
        self.windowNew.filemanager.hideColumn(1)
        self.windowNew.filemanager.hideColumn(2)
        self.windowNew.filemanager.hideColumn(3)

        self._file_selection_model = QtCore.QItemSelectionModel(self.model)
        self._file_selection_model.selectionChanged.connect(self.newFun)

        self.windowNew.filemanager.setAnimated(True)
        self.windowNew.filemanager.setIndentation(20)
        self.windowNew.filemanager.setHeaderHidden(True)
        self.windowNew.filemanager.setSortingEnabled(False)
        self.windowNew.filemanager.setDropIndicatorShown(True)
        self.windowNew.filemanager.setRootIsDecorated(True)
        self.windowNew.filemanager.setUniformRowHeights(True)
        self.windowNew.filemanager.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self.windowNew.filemanager.customContextMenuRequested.connect(
            self.showCMFileM)

        self.theFolderPath = path

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)
        self.theCurrentWorkingPath = filePath
        self.fileSelected = filePath

        """ CHECK IF THE FILESELECTED IS PNG JPG FILE OR ANY FOLDER...
        WILL HAVE TO USE REGEX to Identify the images """

        trans = QtCore.QCoreApplication.translate

        if os.path.isdir(filePath):
            print("Selected a Directory")
            self.windowNew.cameraInfo.setDisabled(True)
            self.windowNew.gpsInfo.setDisabled(True)
            self.windowNew.imageOriginInfo.setDisabled(True)
            self.windowNew.imageInfo.setDisabled(True)
        else:
            if self.fileSelected:
                self.windowNew.cameraInfo.setDisabled(False)
                self.windowNew.gpsInfo.setDisabled(False)
                self.windowNew.imageOriginInfo.setDisabled(False)
                self.windowNew.imageInfo.setDisabled(False)

                self.showMetaDataInInfoTab(fileName, trans)

        self.windowNew.heading.setText(trans("MainWindow", fileName))
        self.showImage(filePath)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_doubleClicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        if os.path.isdir(str(filePath)):
            print("\nIt is a directory")
            self.changePathFindFolder(filePath)
            self.windowNew.inputText.setText(str(filePath))
            self.theCurrentWorkingPath = filePath
        else:
            pass

    def showMetaDataInInfoTab(self, fileName, _translate):
        extractedMetaData = {}
        """MAJOR DRAWBACK PNG FILES NOT WORKING : DONE """
        """ DUMP MAKER DATA before importing: DONE """
        if fileName.lower().endswith(('.jpg', '.JPG', '.jpeg', '.JPEG')):
            extractedMetaData = self.metadata.all_meta_data(self.fileSelected)
            self.windowNew.FileName.setText(
                _translate("MainWindow", str(fileName)))
        elif fileName.lower().endswith(('.png', '.PNG')):
            print("PNG Format does not contain metadata")
        else:
            pass

        if extractedMetaData is not None:
            dt, lat, lon, di, wi, he, hr, vr, bi, ma, mo, fs, ex, iso, fo, me, fl = False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False

            for key, value in extractedMetaData.items():
                # print(key, " : ", value)
                # print(extractedMetaData)

                if str(key) == str("DateTime"):
                    self.windowNew.DateTaken.setText(_translate(
                        "MainWindow", str(value.decode('utf-8'))))
                    dt = True
                elif key == str("latitude"):
                    self.windowNew.Latitude.setText(
                        _translate("MainWindow", str(value)))
                    lat = True
                elif key == "longitude":
                    self.windowNew.Longitude.setText(
                        _translate("MainWindow", str(value)))
                    lon = True
                elif key == "Dimension":
                    self.windowNew.Dimension.setText(
                        _translate("MainWindow", str(value)))
                    di = True
                elif key == "ImageWidth":
                    self.windowNew.Width.setText(
                        _translate("MainWindow", str(value)))
                    wi = True
                elif key == "ImageLength":
                    self.windowNew.Height.setText(
                        _translate("MainWindow", str(value)))
                    he = True
                elif key == "XResolution":
                    self.windowNew.HResolution.setText(
                        _translate("MainWindow", str(value)))
                    hr = True
                elif key == "YResolution":
                    self.windowNew.VResolution.setText(
                        _translate("MainWindow", str(value)))
                    vr = True
                elif key == "BitDepth":
                    self.windowNew.BitDepth.setText(
                        _translate("MainWindow", str(value)))
                    bi = True
                elif key == "Make":
                    self.windowNew.Maker.setText(_translate(
                        "MainWindow", str(value.decode('utf-8'))))
                    ma = True
                elif key == "Model":
                    self.windowNew.Model.setText(_translate(
                        "MainWindow", str(value.decode('utf-8'))))
                    mo = True
                elif key == "FNumber":
                    self.windowNew.Fstop.setText(
                        _translate("MainWindow", str(value)))
                    fs = True
                elif key == "ExposureTime":
                    self.windowNew.ExposureTime.setText(
                        _translate("MainWindow", str(value)))
                    ex = True
                elif key == "ISOSpeedRatings":
                    self.windowNew.ISOspeed.setText(
                        _translate("MainWindow", str(value)))
                    iso = True
                elif key == "FocalLength":
                    self.windowNew.FocalLength.setText(
                        _translate("MainWindow", str(value)))
                    fo = True
                elif key == "MeteringMode":
                    self.windowNew.MeteringMode.setText(
                        _translate("MainWindow", str(value)))
                    me = True
                elif key == "Flash":
                    self.windowNew.FlashMode.setText(
                        _translate("MainWindow", str(value)))
                    fl = True
                else:
                    pass

            if dt == False:
                self.windowNew.DateTaken.setText(
                    _translate("MainWindow", "None"))
            if lat == False:
                self.windowNew.Latitude.setText(
                    _translate("MainWindow", "None"))
            if lon == False:
                self.windowNew.Longitude.setText(
                    _translate("MainWindow", "None"))
            if di == False:
                self.windowNew.Dimension.setText(
                    _translate("MainWindow", "None"))
            if wi == False:
                self.windowNew.Width.setText(_translate("MainWindow", "None"))
            if he == False:
                self.windowNew.Height.setText(_translate("MainWindow", "None"))
            if hr == False:
                self.windowNew.HResolution.setText(
                    _translate("MainWindow", "None"))
            if vr == False:
                self.windowNew.VResolution.setText(
                    _translate("MainWindow", "None"))
            if bi == False:
                self.windowNew.BitDepth.setText(
                    _translate("MainWindow", "None"))
            if ma == False:
                self.windowNew.Maker.setText(_translate("MainWindow", "None"))
            if mo == False:
                self.windowNew.Model.setText(_translate("MainWindow", "None"))
            if fs == False:
                self.windowNew.Fstop.setText(_translate("MainWindow", "None"))
            if ex == False:
                self.windowNew.ExposureTime.setText(
                    _translate("MainWindow", "None"))
            if iso == False:
                self.windowNew.ISOspeed.setText(
                    _translate("MainWindow", "None"))
            if fo == False:
                self.windowNew.FocalLength.setText(
                    _translate("MainWindow", "None"))
            if me == False:
                self.windowNew.MeteringMode.setText(
                    _translate("MainWindow", "None"))
            if fl == False:
                self.windowNew.FlashMode.setText(
                    _translate("MainWindow", "None"))

        dt, lat, lon, di, wi, he, hr, vr, bi, ma, mo, fs, ex, iso, fo, me, fl = False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False

    def showCMFileM(self):
        """ Context menu for file manager """
        """ undo.. redo.. (prev.. forward).. open.. properties.. """
        pass

    def newFun(self):
        print("changed")

    def showImage(self, filePath):
        self.image_path = str(filePath)
        if os.path.isfile(self.image_path):
            self.viewer.setPhoto(QtGui.QPixmap(self.image_path))

    def browsePics(self):
        dialog = QtWidgets.QFileDialog
        directory = dialog.getExistingDirectory(
            self, "Open Directory", ".", dialog.ShowDirsOnly | dialog.DontResolveSymlinks)
        allFilesList = glob.glob(str(directory)+r"/**/*.jpeg", recursive=True)
        allFilesList.extend(
            glob.glob(str(directory)+r"/**/*.jpg", recursive=True))
        # allFilesList.extend(glob.glob(str(directory)+r"/**/*.JPG",recursive=True))
        # allFilesList.extend(glob.glob(str(directory)+r"/**/*.JPEG",recursive=True))
        # print(allFilesList)
        if allFilesList:
            self.importPics()

    def importPics(self):
        _translate = QtCore.QCoreApplication.translate
        self.successImport.setText(_translate(
            "MainWindow", "Successfully imported all photos"))

    """ TRAINING FUNCTIONS """

    def browseTrainPics(self):
        dialog = QtWidgets.QFileDialog
        directory = dialog.getExistingDirectory(
            self, "Open Directory", ".", dialog.ShowDirsOnly | dialog.DontResolveSymlinks)
        self.folderTrainName = directory
        # print(self.folderTrainName)
        if self.folderTrainName is not None:
            self.importTrainPics()

    def importTrainPics(self):
        _translate = QtCore.QCoreApplication.translate
        self.foundFacesTrain.setText(_translate(
            "MainWindow", "Found images for training"))
        self.statusbar.showMessage("")

    def trainCallFunc(self):
        if os.path.exists(str(self.folderTrainName)+"/trained_knn_model.clf"):
            self.model_saved_on_path = str(
                self.folderTrainName)+"/trained_knn_model.clf"
            self.statusbar.showMessage("Trained File Exists")
        else:
            if self.folderTrainName is not "":
                self.statusbar.showMessage("Training KNN Classifier... ")
                self.classifier = self.facerec.train(str(self.folderTrainName), model_save_path=str(
                    self.folderTrainName)+"/trained_knn_model.clf", n_neighbors=2)
                self.model_saved_on_path = str(
                    self.folderTrainName)+"/trained_knn_model.clf"
                if self.classifier is not None:
                    self.trainingComplete()
                    self.statusbar.showMessage("Finished.")
            else:
                self.statusbar.showMessage(
                    "Choose folder containing training images first.")

    def trainingClass(self):
        # print("YOLO")
        _translate = QtCore.QCoreApplication.translate
        self.compl_train.setText(_translate(
            "MainWindow", "Training KNN classifier..."))

    def trainingComplete(self):
        _translate = QtCore.QCoreApplication.translate
        self.compl_train.setText(_translate(
            "MainWindow", "Training Complete.."))

    """ TESTING FUNCTIONS """

    def browseTestPics(self):
        dialog = QtWidgets.QFileDialog
        directory = dialog.getExistingDirectory(
            self, "Open Test Directory", ".", dialog.ShowDirsOnly | dialog.DontResolveSymlinks)
        allFilesList = glob.glob(str(directory)+r"/**/*.jpeg", recursive=True)
        allFilesList.extend(
            glob.glob(str(directory)+r"/**/*.jpg", recursive=True))
        # print(allFilesList)
        self.filesTestNameList = allFilesList
        self.folderTestName = directory
        if self.folderTestName is not None:
            self.importTestPics()

    def importTestPics(self):
        _translate = QtCore.QCoreApplication.translate
        self.recog_faces.setText(_translate(
            "MainWindow", "Found images for testing"))
        self.statusbar.showMessage("")

    def testCallFunc(self):
        self.statusbar.showMessage("Testing")
        for oneFileName in self.filesTestNameList:
            allNames = []
            count = 0
            self.predictions = self.facerec.predict(
                str(oneFileName), model_path=self.model_saved_on_path)
            if self.predictions is not None:
                self.testingComplete()
                for name, (top, right, bottom, left) in self.predictions:
                    if name is "unknown":
                        count = count + 1
                    else:
                        allNames.append(name)

                if allNames:
                    print("-- Found " + ",".join(allNames) + " and " +
                          str(count) + " unknown persons in " + oneFileName + " -- ")
                else:
                    print("-- Found " + str(count) +
                          " unknown people in " + oneFileName + " -- ")

    def testingComplete(self):
        _translate = QtCore.QCoreApplication.translate
        self.compl_test.setText(_translate("MainWindow", "Testing Complete.."))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Gallary"))

        self.importFilePathButton.setText(
            _translate("MainWindow", "Choose Folder"))
        self.chooseMainPath.setText(_translate(
            "MainWindow", "Choose folder which contains photos:"))
        self.chooseTrainPath.setText(_translate(
            "MainWindow", "Choose path of folder which contains training photos:"))
        self.train_path_import_button.setText(
            _translate("MainWindow", "Choose Training Images"))
        self.train_button.setText(_translate("MainWindow", "Train Images"))
        self.test_button.setText(_translate("MainWindow", "Test Images"))
        self.chooseTestPath.setText(_translate(
            "MainWindow", "Choose path of folder which contains testing photos:"))
        self.test_path_import_button.setText(
            _translate("MainWindow", "Choose Testing Images"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gallary(MainWindow)
    sys.exit(app.exec_())
