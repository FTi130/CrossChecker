
# -*- coding: utf-8 -*-
import sys
import os 
from PySide import QtGui, QtCore
import numpy as np
import cv2
import subprocess
import matplotlib.pyplot as plt

#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
global info
info = []
sys.setrecursionlimit(900)


class TestListView(QtGui.QListWidget):
    fileDropped = QtCore.Signal(list)

    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)  #
        self.setIconSize(QtCore.QSize(300, 300))



    def dragEnterEvent(self, event):
        self.setStyleSheet("background-color: rgb(60, 73, 76);")
        if event.mimeData().hasUrls:
            event.accept()

        else:
            event.ignore()

    def dragMoveEvent(self, event):
        #self.setStyleSheet("background-color: rgb(100, 63, 66);")
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.setStyleSheet("background-color: rgb(35, 40, 45);")##################### rgb(50, 51, 53)
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                try:
                    links.append(str(url.toLocalFile()))
                except UnicodeEncodeError:
                    msg = QtGui.QMessageBox()
                    msg.setIcon(QtGui.QMessageBox.Critical)
                    msg.setText("Don't feed me with some weird files")
                    msg.setInformativeText('Check if there is a Russian name in {}'.format(str(url).split('///')[1]))
                    msg.setWindowTitle("Wait a second")
                    msg.exec_()

            self.fileDropped.emit(links)
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        self.clearSelection()


#################
#################

class MainForm(QtGui.QMainWindow):

    fileChoosen = QtCore.Signal()
    resized = QtCore.Signal()
    global ii
    ii = 0

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)

        self.view.fileDropped.connect(self.ffprobe)  # connection to the main function ffprobe

        self.setCentralWidget(self.view)
        #self.move(QtGui.QApplication.desktop().screen().rect().center() - self.rect().center())  ### lastchange centre
        # Title
        self.setWindowTitle("SILA SVETA OpenCV Checker")
        # logo
        self.setWindowIcon(QtGui.QIcon('output_checker_icon.ico'))
        # Resize Main Window
        self.resize(1400, 1020) # 1400, 1020



        # Enabling of Multiselection goes here

        self.view.setSelectionMode(self.view.SingleSelection)
        self.view.setSelectionBehavior(self.view.SelectRows)
        #self.view.setSelectionMode(self.view.A)
        #### WTF
        self.view.setEditTriggers(self.view.NoEditTriggers)
        self.view.setFocusPolicy(QtCore.Qt.NoFocus)





        self.setStyleSheet("background-color: rgb(55, 60, 65);\n"  # (100,100,100)
                           "border-radius: 2px;\n"
                           "color: rgb(255, 255, 255);\n"
                           "selection-background-color: rgb(120, 160, 230);")


        #self.view.setStyleSheet("background-color: rgb(35, 40, 45); alternate-background-color: rgb(90,255, 90); color: rgb(255, 255, 255);")      #######   color font changes here                                #('font: bold 8px;') background-color: rgb(100, 100, 100)

        self.view.setStyleSheet(""" 
                                    QTableWidget:hover { background-color: rgb(60, 73, 76); alternate-background-color: rgb(90,255, 90); color: rgb(255, 255, 255) }
                                    QTableWidget:!hover { background-color: rgb(35, 40, 45); alternate-background-color: rgb(90,255, 90); color: rgb(255, 255, 255)) }

                                """)


        self.view.setMouseTracking(True)

        # ComboBoxes

        self.menu = QtGui.QWidget()


        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())

        spacerItem = QtGui.QSpacerItem(10, 100, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)


        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMinimumSize(QtCore.QSize(300, 100))
        self.menu.setObjectName("menu")




        self.listwidget = QtGui.QListWidget(self)    #raw.
        #self.listwidget.setStyleSheet('background-color: rgb(35, 75, 45);font: 14px;') #raw.

        #############################################

        self.menu.textDrop = QtGui.QLabel()
        self.menu.textDrop.setText("You can drop folder on the right")




        # Buttons

        self.menu.buttonex = QtGui.QPushButton('Browse', self)   #Former Exit
        self.menu.buttonclear = QtGui.QPushButton('Clear All', self)

        self.menu.buttonex.setMinimumSize(QtCore.QSize(0, 30))
        self.menu.buttonclear.setMinimumSize(QtCore.QSize(0, 30))

        # Layouts
        self.menu.h2Box = QtGui.QVBoxLayout()
        self.menu.vbox = QtGui.QVBoxLayout()
        self.menu.hbox = QtGui.QVBoxLayout()
        self.menu.mybox = QtGui.QHBoxLayout()

        self.menu.vbox.setContentsMargins(15, 15, -1, 20)  #-1 0 -1 -1


        self.menu.vbox.addWidget(self.menu.textDrop)


        # GroupBox

        self.groupBox_Properties = QtGui.QGroupBox(self.menu)
        self.groupBox_Properties.setObjectName("groupBox_Properties")

        font = QtGui.QFont()
        font.setPointSize(8)

        self.groupBox_Properties.setFont(font)
        #self.groupBox_Properties.setStyleSheet("background: red;")
        self.formLayout = QtGui.QFormLayout(self.groupBox_Properties)
        self.formLayout.setContentsMargins(0, 26, 0, 16)
        self.formLayout.setSpacing(10)


        self.menu.vbox.addWidget(self.groupBox_Properties)

        #self.menu.vbox.addItem(spacerItem) ############################## add smth indications buttons

        self.menu.vbox.addWidget(self.menu.buttonex)   #vbox
        self.menu.vbox.addWidget(self.menu.buttonclear) #vbox

        #self.menu.vbox.addWidget(self.menu.buttonsortname)

        #### Adding spacer

        self.menu.vbox.addItem(spacerItem)

        #self.menu.vbox.addLayout(self.menu.mybox, stretch=True)
        self.menu.vbox.addLayout(self.menu.h2Box, stretch=True)
        self.menu.vbox.addLayout(self.menu.hbox, stretch=True)
        #self.menu.vbox.addLayout(self.menu.mybox, stretch=True)

        #self.menu.hbox.addLayout(self.menu.vbox)

        self.menu.setLayout(self.menu.vbox)
        self.setLayout(self.menu.h2Box)

        self.setMenuWidget(self.menu)               # Here menu Widget becomes Menu on top of the window______________________________
        #self.menu.move(0, 500)


        self.dockMenu = QtGui.QDockWidget(str(""), self)
        self.dockMenu.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)

        self.dockMenu.setWidget(self.menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockMenu)

        self.dockMenu.setFeatures(QtGui.QDockWidget.DockWidgetMovable == False) #QtGui.QDockWidget.DockWidgetFloatable)# | QtGui.QDockWidget.DockWidgetMovable)
        self.dockMenu.setTitleBarWidget(QtGui.QWidget(None))

############################################################
############################################################
        # GroupBox


   #########################################################



        ##########
        ##########
        # Setting a style for comboboxes and buttons using CSS


        self.menu.buttonex.setStyleSheet("""
                    QPushButton:hover { background-color: rgb(105, 110, 115) }
                    QPushButton:!hover { background-color: rgb( 95, 100, 105) }

                    QPushButton:pressed { background-color: rgb(125, 130, 135); }
                """)




        self.menu.buttonclear.setStyleSheet("""
            QPushButton:hover { background-color: rgb(105, 110, 115) }
            QPushButton:!hover { background-color: rgb( 95, 100, 105) }

            QPushButton:pressed { background-color: rgb(125, 130, 135); }
        """)


        self.menu.textDrop.setStyleSheet('font: 12px;color:white;') # MS Shell Dlg 2 20px


        self.menu.buttonclear.clicked.connect(self.cleartable)
        self.menu.buttonex.clicked.connect(self.openFileDialog)         # Exit button    openFileDialog   ButtonEx









    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainForm, self).resizeEvent(event)

    # Resize columns after resizing MainWindow


    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Delete:
            self._del_item()

    def _del_item(self):
        self.view.clear()

    # Clear the table function
    def cleartable(self):
        self.view.clear()



    def openFileDialog(self):
        """
        Opens a file dialog
        """
        import os
        path, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        #self.label.setText(path)

        f=[]
        f.append(path)
        
        

        self.ffprobe(f)                ############################## HERE adding


    def openDirectoryDialog(self):
        """
        Opens a dialog to allow user to choose a directory
        """
        flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        d = directory = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory", os.getcwd(),flags)
        #self.label.setText(d)


        #Following functions together with their buttons are created because when SetSortingEnabled is True and you sort items in the column pressing on the ColumnHeader
        # after adding a next batch of urls your rows will mess up. Idk where is the reason, probably, due to adding an empty row affter execution of all ffprobe() actions



    # Exit function
    def ButtonEx(self):
        app.exit()
    
    # Main function. It is working with FFprobe and add data to the table
    def ffprobe(self, f):
        neededFiles = []
        for url in f:
            # case if dropped item is a file
            # starting a pathfinder and get all the sequence from its folder
            if os.path.isfile(url):
                # print url
                file_without_path = url.split('/')[-1]
                path = url.split('/')[:-1]

                path = '/'.join(path)
                print path

                print file_without_path
                base_name, ext = os.path.splitext(file_without_path)

                print base_name
                # print ext
                everyname = base_name.split('_')[:-1]
                counter = base_name.split('_')[-1]

                os.chdir(path)
                for i in os.listdir(path):
                    i_without_path = i.split('/')[-1]
                    base_name_i, ext_i = os.path.splitext(i_without_path)
                    everyname_i = base_name_i.split('_')[:-1]
                    counter_i = base_name_i.split('_')[-1]

                    if everyname == everyname_i and counter != counter_i:
                        neededFiles.append(i)

                print neededFiles

                FirstFileName = neededFiles[1]

                def GetSequenceName(
                        FirstFileName):  # GetSequenceName processes file name and converts it to sequence name, adding pattern like %05d
                    start = '_'
                    end = '.'

                    symbols = list(FirstFileName)
                    i = 0
                    pos1 = 0
                    pos2 = 0
                    for symbol in symbols:
                        if symbol == start:
                            pos1 = i
                        elif symbol == end:
                            pos2 = i
                        i += 1
                    result = FirstFileName[pos1 + 1:pos2]
                    count = len(result)
                    return (FirstFileName[:pos1] + '_%0' + str(count) + 'd' + FirstFileName[pos2:])

                name = str(GetSequenceName(FirstFileName))

                ######
                # lists = os.listdir(url) # dir is your directory path
                numberfiles = len(neededFiles)
                neededFiles.sort()
                for pics in neededFiles:
                    # print pics
                    img = cv2.imread(pics, cv2.IMREAD_COLOR)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    graycenter = gray[int(gray.shape[0] / 2), int(gray.shape[1] / 2)]
                    grayleftUpper = gray[int(gray.shape[0] / 4), int(gray.shape[1] / 4)]

                    threefour = 4
                    thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)[1]
                    fourthree = 4 / 3

                    thrcenter = thresh[int(thresh.shape[0] / 2), int(thresh.shape[1] / (2))]
                    thrleftUpper = thresh[int(thresh.shape[0] / (4)), int(thresh.shape[1] / 4)]
                    thrrightUpper = thresh[int(thresh.shape[0] / (1.33333333)), int(thresh.shape[1] / 4)]
                    thrrightLower = thresh[int(thresh.shape[0] / (1.33333333)), int(thresh.shape[1] / (1.33333333))]
                    thrleftLower = thresh[int(thresh.shape[0] / 4), int(thresh.shape[1] / (1.33333333))]

                    randompoint1 = thresh[int(thresh.shape[0] / 4), int(thresh.shape[1] / 2.5)]
                    randompoint2 = thresh[int(thresh.shape[0] / 3.7), int(thresh.shape[1] / (1.8))]

                    try:
                        colorCenter = img[int(img.shape[0] / 2), int(img.shape[1] / 2)]
                    except AttributeError:
                        message = str(pics) + " looks like some shit"
                        item = QtGui.QListWidgetItem(message, self.view)

                    #if thrleftLower == thrrightLower == thrrightUpper == thrleftUpper == thrcenter:

                    if (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint1) \
                            and (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint2):
                        # print "Picture is probably with the cross"
                        try:
                            message = str(pics) + " is probably with cross"
                            item = QtGui.QListWidgetItem(message, self.view)
                        except AttributeError:
                            message = str(pics) + " looks like some shit"
                            item = QtGui.QListWidgetItem(message, self.view)

                    app.processEvents()

            else:
                # case if dropped item is a folder with a sequence inside
                # print url
                if os.path.exists(url):
                    os.chdir(url)
                    for pics in os.listdir(url):
                        # print pics
                        img = cv2.imread(pics, cv2.IMREAD_COLOR)

                        # #### Start changing
                        try:
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        except AttributeError:
                            message = str(pics) + " looks like some shit"
                            item = QtGui.QListWidgetItem(message, self.view)
                        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        graycenter = gray[int(gray.shape[0] / 2), int(gray.shape[1] / 2)]
                        grayleftUpper = gray[int(gray.shape[0] / 4), int(gray.shape[1] / 4)]

                        threefour = 4
                        thresh = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)[1]
                        fourthree = 4 / 3

                        thrcenter = thresh[int(thresh.shape[0] / 2), int(thresh.shape[1] / (2))]
                        thrleftUpper = thresh[int(thresh.shape[0] / (4)), int(thresh.shape[1] / 4)]
                        thrrightUpper = thresh[int(thresh.shape[0] / (1.33333333)), int(thresh.shape[1] / 4)]
                        thrrightLower = thresh[int(thresh.shape[0] / (1.33333333)), int(thresh.shape[1] / (1.33333333))]
                        thrleftLower = thresh[int(thresh.shape[0] / 4), int(thresh.shape[1] / (1.33333333))]

                        randompoint1 = thresh[int(thresh.shape[0] / 4), int(thresh.shape[1] / 2.5)]
                        randompoint2 = thresh[int(thresh.shape[0] / 3.7), int(thresh.shape[1] / (1.8))]

                        randompoint3 = thresh[int(thresh.shape[0] / 2), int(thresh.shape[1] / (1.33333333))]
                        randompoint4 = thresh[int(thresh.shape[0] / 1.33333333), int(thresh.shape[1] / 2)]


                        try:
                            colorCenter = img[int(img.shape[0] / 2), int(img.shape[1] / 2)]
                        except AttributeError:
                            message = str(pics) + " looks like some shit"
                            item = QtGui.QListWidgetItem(message, self.view)

                        #if thrleftLower == thrrightLower == thrrightUpper == thrleftUpper ==thrcenter:

                        if (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint1) \
                                and (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint2) \
                                and (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint3) \
                                and (thrleftLower == thrrightLower == thrrightUpper == thrleftUpper != randompoint4):

                            try:
                                icon = QtGui.QIcon(pics)
                                pixmap = icon.pixmap(800, 800)
                                icon = QtGui.QIcon(pixmap)
                                message = str(pics) + " is probably with cross" + "\n" +\
                                          str(thrleftLower) + "__" +\
                                          str(thrrightLower) + "__" +\
                                          str(thrrightUpper) + "__" +\
                                          str(thrleftUpper) + ", Center: " +\
                                          str(thrcenter) + "     Random1: " +\
                                          str(randompoint1) + "  Random2: " + \
                                          str(randompoint2)


                                item = QtGui.QListWidgetItem(message, self.view)
                                item.setIcon(icon)

                            except AttributeError:
                                message = str(pics) + " looks like some shit"
                                icon = QtGui.QIcon(pics)
                                pixmap = icon.pixmap(800, 800)
                                icon = QtGui.QIcon(pixmap)
                                item = QtGui.QListWidgetItem(message, self.view)
                                item.setIcon(icon)

                        app.processEvents()


def main():
    global app
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
