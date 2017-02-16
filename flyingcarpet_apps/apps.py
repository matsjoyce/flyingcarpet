import itertools

from PyQt5 import QtCore, QtGui, QtWidgets

import flyingcarpet
from flyingcarpet import build


class AppsApp(flyingcarpet.App):
    NAME = "Apps"
    GENERIC_NAME = "App collection"
    DESCRIPTION = "A list of all flyingcarpet apps"
    VERSION = (0, 1)
    ICON = "view-list-details"
    CATEGORIES = {flyingcarpet.Category.System}

    def __init__(self):
        super().__init__()

        self.tw = QtWidgets.QTreeWidget(self)
        self.tw.setHeaderLabels(["Name", "Value"])

        fb = build.FileBuilder(build.FileBuilder.APPS_DIR, build.FileBuilder.APPS_DIR)
        key = lambda app: app.PATH
        for path, apps in itertools.groupby(sorted(fb.apps, key=key), key=key):
            path_item = QtWidgets.QTreeWidgetItem(self.tw, [str(path), ""])
            for app in apps:
                app_item = QtWidgets.QTreeWidgetItem(path_item, [app.NAME, ".".join(map(str, app.VERSION))])
                for key, value in app.app_data():
                    key_item = QtWidgets.QTreeWidgetItem(app_item, [key, value])
        self.tw.collapsed.connect(self.tw_resize)
        self.tw.expanded.connect(self.tw_resize)
        self.tw_resize()
        self.centrallayout.addWidget(self.tw, 0, 0)

    def tw_resize(self):
        self.tw.resizeColumnToContents(0)
