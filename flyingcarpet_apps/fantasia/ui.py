# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fantasia/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 601)
        icon = QtGui.QIcon.fromTheme("player-volume")
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.playlist_tab = QtWidgets.QWidget()
        self.playlist_tab.setObjectName("playlist_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.playlist_tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget.addTab(self.playlist_tab, "")
        self.media_tab = QtWidgets.QWidget()
        self.media_tab.setObjectName("media_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.media_tab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget.addTab(self.media_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.control_toolbar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.control_toolbar.sizePolicy().hasHeightForWidth())
        self.control_toolbar.setSizePolicy(sizePolicy)
        self.control_toolbar.setMovable(False)
        self.control_toolbar.setIconSize(QtCore.QSize(32, 32))
        self.control_toolbar.setFloatable(False)
        self.control_toolbar.setObjectName("control_toolbar")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.control_toolbar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setStyleSheet("QStatusBar { background-color: black; color: white}")
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 797, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuAdd = QtWidgets.QMenu(self.menuBar)
        self.menuAdd.setObjectName("menuAdd")
        MainWindow.setMenuBar(self.menuBar)
        self.actionPlay = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.actionPlay.setIcon(icon)
        self.actionPlay.setObjectName("actionPlay")
        self.actionStop = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-playback-stop")
        self.actionStop.setIcon(icon)
        self.actionStop.setObjectName("actionStop")
        self.actionPause = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-playback-pause")
        self.actionPause.setIcon(icon)
        self.actionPause.setObjectName("actionPause")
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-skip-backward")
        self.actionPrevious.setIcon(icon)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-skip-forward")
        self.actionNext.setIcon(icon)
        self.actionNext.setObjectName("actionNext")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.actionRemove.setIcon(icon)
        self.actionRemove.setObjectName("actionRemove")
        self.actionMove_Up = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("arrow-up")
        self.actionMove_Up.setIcon(icon)
        self.actionMove_Up.setObjectName("actionMove_Up")
        self.actionMove_Down = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("arrow-down")
        self.actionMove_Down.setIcon(icon)
        self.actionMove_Down.setObjectName("actionMove_Down")
        self.actionRandomize = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-playlist-shuffle")
        self.actionRandomize.setIcon(icon)
        self.actionRandomize.setObjectName("actionRandomize")
        self.actionLoop = QtWidgets.QAction(MainWindow)
        self.actionLoop.setCheckable(True)
        icon = QtGui.QIcon.fromTheme("media-playlist-repeat")
        self.actionLoop.setIcon(icon)
        self.actionLoop.setObjectName("actionLoop")
        self.actionAdd = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.actionAdd.setIcon(icon)
        self.actionAdd.setObjectName("actionAdd")
        self.actionClear = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-clear-list")
        self.actionClear.setIcon(icon)
        self.actionClear.setObjectName("actionClear")
        self.actionSeek_Backward = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-seek-backward")
        self.actionSeek_Backward.setIcon(icon)
        self.actionSeek_Backward.setObjectName("actionSeek_Backward")
        self.actionSeek_Forward = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-seek-forward")
        self.actionSeek_Forward.setIcon(icon)
        self.actionSeek_Forward.setObjectName("actionSeek_Forward")
        self.actionAdd_Music_File = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionAdd_Music_File.setIcon(icon)
        self.actionAdd_Music_File.setObjectName("actionAdd_Music_File")
        self.actionAdd_Music_Folder = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actionAdd_Music_Folder.setIcon(icon)
        self.actionAdd_Music_Folder.setObjectName("actionAdd_Music_Folder")
        self.control_toolbar.addAction(self.actionPlay)
        self.control_toolbar.addAction(self.actionPause)
        self.control_toolbar.addAction(self.actionStop)
        self.control_toolbar.addSeparator()
        self.control_toolbar.addAction(self.actionPrevious)
        self.control_toolbar.addAction(self.actionSeek_Backward)
        self.control_toolbar.addAction(self.actionSeek_Forward)
        self.control_toolbar.addAction(self.actionNext)
        self.control_toolbar.addSeparator()
        self.control_toolbar.addAction(self.actionAdd)
        self.control_toolbar.addAction(self.actionRemove)
        self.control_toolbar.addAction(self.actionClear)
        self.control_toolbar.addSeparator()
        self.control_toolbar.addAction(self.actionMove_Up)
        self.control_toolbar.addAction(self.actionMove_Down)
        self.control_toolbar.addSeparator()
        self.control_toolbar.addAction(self.actionRandomize)
        self.control_toolbar.addAction(self.actionLoop)
        self.menuAdd.addAction(self.actionAdd_Music_File)
        self.menuAdd.addAction(self.actionAdd_Music_Folder)
        self.menuBar.addAction(self.menuAdd.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "fantasia"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.playlist_tab), _translate("MainWindow", "Playlist"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.media_tab), _translate("MainWindow", "All Media"))
        self.control_toolbar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuAdd.setTitle(_translate("MainWindow", "A&dd"))
        self.actionPlay.setText(_translate("MainWindow", "Play"))
        self.actionPlay.setShortcut(_translate("MainWindow", "Space"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionPause.setShortcut(_translate("MainWindow", "Space"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous"))
        self.actionPrevious.setShortcut(_translate("MainWindow", "Shift+Left"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionNext.setShortcut(_translate("MainWindow", "Shift+Right"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))
        self.actionRemove.setShortcut(_translate("MainWindow", "Backspace"))
        self.actionMove_Up.setText(_translate("MainWindow", "Move Up"))
        self.actionMove_Down.setText(_translate("MainWindow", "Move Down"))
        self.actionRandomize.setText(_translate("MainWindow", "Randomize"))
        self.actionRandomize.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionLoop.setText(_translate("MainWindow", "Loop"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionClear.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionSeek_Backward.setText(_translate("MainWindow", "Seek Backward"))
        self.actionSeek_Backward.setToolTip(_translate("MainWindow", "Seek Backward"))
        self.actionSeek_Backward.setShortcut(_translate("MainWindow", "Left"))
        self.actionSeek_Forward.setText(_translate("MainWindow", "Seek Forward"))
        self.actionSeek_Forward.setShortcut(_translate("MainWindow", "Right"))
        self.actionAdd_Music_File.setText(_translate("MainWindow", "&Add Music File"))
        self.actionAdd_Music_File.setToolTip(_translate("MainWindow", "Add Music File"))
        self.actionAdd_Music_Folder.setText(_translate("MainWindow", "Add &Music Folder"))
        self.actionAdd_Music_Folder.setToolTip(_translate("MainWindow", "Add Music Folder"))

