from PyQt5 import QtCore, QtGui, QtWidgets

import flyingcarpet
import sys
import pathlib
import potash
from potash.qt3 import object_view, object_model, object_edit_widget, source_unlock_dialog, displays

sys.path.insert(0, "/home/matthew/.local/share/tasksd/tasks/")

import twitter_objs
import rss_feed_objs


class TypeDisplay(displays.Display):
    def display_role(self, obj, value, attr):
        if value is twitter_objs.TwitterState:
            return "Twitter"
        else:
            return "RSS"

    sorting_key = display_role


class TNSApp(flyingcarpet.App):
    NAME = "TNS"
    GENERIC_NAME = "Feed manager"
    DESCRIPTION = "Tasksd feed manager"
    VERSION = (0, 1)
    ICON = "feed-subscribe"
    CATEGORIES = {flyingcarpet.Category.Network}
    SUBCATEGORIES = {flyingcarpet.SubCategory.Feed}

    def __init__(self):
        super().__init__(with_toolbar=True, maximized=True)

        model = object_model.ObjectModel(potash.user_source(), self)
        model.setHeaders([
            object_model.ObjectModelHeader("__class__", display=TypeDisplay(), title="Type"),
            object_model.ObjectModelHeader(self.value_attr, title="Value")
            ])
        model.setFilter(type=(twitter_objs.TwitterState, rss_feed_objs.RSSState))

        self.view = object_view.ObjectView(self)
        self.view.setSortingEnabled(True)
        self.view.setModel(model)
        self.view.edit_action = self.view.view_selected
        self.centrallayout.addWidget(self.view)

        add_action = QtWidgets.QAction(QtGui.QIcon.fromTheme("im-twitter"), "Add Twitter", self)
        add_action.triggered.connect(self.add_twitter)
        self.toolbar.addAction(add_action)

        add_action = QtWidgets.QAction(QtGui.QIcon.fromTheme("feed-subscribe"), "Add RSS", self)
        add_action.triggered.connect(self.add_rss)
        self.toolbar.addAction(add_action)

        remove_action = QtWidgets.QAction(QtGui.QIcon.fromTheme("list-remove"), "Remove", self)
        remove_action.setShortcut("Ctrl+R")
        remove_action.triggered.connect(self.remove_feed)
        self.toolbar.addAction(remove_action)

    def value_attr(self, obj):
        if type(obj) is twitter_objs.TwitterState:
            return "username"
        else:
            return "feed_url"

    def add_twitter(self):
        state = twitter_objs.TwitterState(self.view.model().source)
        if not object_edit_widget.ObjectEditDialog.edit([state], self.view.model().displayed_headers(), self):
            state.destroy()

    def add_rss(self):
        state = rss_feed_objs.RSSState(self.view.model().source)
        if not object_edit_widget.ObjectEditDialog.edit([state], self.view.model().displayed_headers(), self):
            state.destroy()

    def remove_feed(self):
        for obj in self.view.selectedObjects():
            obj.destroy()
        self.view.model().source.commit()
