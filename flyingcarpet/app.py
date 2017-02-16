import sys
import enum

from PyQt5 import QtCore, QtGui, QtWidgets

from .ui import about
from . import build


class App(QtWidgets.QMainWindow):
    ICON = "applications-other"
    DESCRIPTION = ""
    SUBCATEGORIES = set()
    ADD_PREFIX = True
    LAUNCHER_NAME = None

    def __init__(self, with_toolbar=False, maximized=False):
        self.application = QtWidgets.QApplication(sys.argv)
        super().__init__()

        self.icon = QtGui.QIcon.fromTheme(self.ICON)

        self.setWindowTitle(("flyingcarpet::" if self.ADD_PREFIX else "") + self.NAME)
        self.setWindowIcon(self.icon)

        self.quit_shortcut = QtWidgets.QShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q, self)
        self.quit_shortcut.activated.connect(self.close)

        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.help_menu = QtWidgets.QMenu("Help", self.menubar)
        self.about_action = QtWidgets.QAction(self.icon, f"About {self.NAME}", self.help_menu)
        self.about_action.triggered.connect(self.on_about_action)
        self.help_menu.addAction(self.about_action)

        if with_toolbar:
            self.toolbar = QtWidgets.QToolBar(self)
            self.toolbar.setMovable(False)
            self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            self.toolbar.setFloatable(False)
            self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        if maximized:
            self.setWindowState(QtCore.Qt.WindowMaximized)

        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)
        self.centrallayout = QtWidgets.QGridLayout(self.central)
        self.central.setLayout(self.centrallayout)

    @property
    def menuBar(self):
        return self.menubar

    @menuBar.setter
    def menuBar(self, value):
        value.setParent(None)

    @property
    def toolBar(self):
        return self.toolbar

    @toolBar.setter
    def toolBar(self, value):
        value.setParent(None)

    @classmethod
    def app_data(cls):
        data = []
        data.append(("Name", cls.NAME))
        data.append(("Generic name", cls.GENERIC_NAME))
        data.append(("Class name", cls.__name__))
        data.append(("Load path", str(build.FileBuilder.APPS_DIR / cls.PATH)))
        if cls.DESCRIPTION:
            data.append(("Description", cls.DESCRIPTION))
        data.append(("Version", ".".join(map(str, cls.VERSION))))
        data.append(("Categories", ", ".join(i.value for i in cls.CATEGORIES)))
        data.append(("Subcategories", ", ".join(i.value[0] for i in cls.SUBCATEGORIES)))
        data.append(("Icon", cls.ICON))
        return data

    def on_about_action(self):
        about.AboutDialog.about(type(self), self)

    def post_init(self):
        self.menubar.addMenu(self.help_menu)

    def run(self):
        self.post_init()
        self.show()
        return self.application.exec_()

    @classmethod
    def __init_subclass__(cls):
        assert hasattr(cls, "NAME")
        assert hasattr(cls, "VERSION")
        assert hasattr(cls, "GENERIC_NAME")
        assert hasattr(cls, "CATEGORIES")
        assert isinstance(cls.CATEGORIES, set)
