from PyQt5 import QtCore, QtGui, QtWidgets

import flyingcarpet
import potash
from potash.qt3 import object_view, object_model, object_edit_widget, source_unlock_dialog


class NotesApp(flyingcarpet.App):
    NAME = "Notes"
    GENERIC_NAME = "Note Taker"
    DESCRIPTION = "A small note taking app"
    VERSION = (0, 1)
    ICON = "note"
    CATEGORIES = {flyingcarpet.Category.Utility}
    SUBCATEGORIES = {flyingcarpet.SubCategory.TextEditor}

    def __init__(self):
        super().__init__(with_toolbar=True, maximized=True)

        model = object_model.ObjectModel(potash.user_source(), self)
        model.setHeaders([
            object_model.ObjectModelHeader("key"),
            object_model.ObjectModelHeader("summary"),
            object_model.ObjectModelHeader("tags")
            ])
        model.setFilter(type=potash.builtin_objects.Note)

        self.view = object_view.ObjectView(self)
        self.view.setSortingEnabled(True)
        self.view.setModel(model)
        self.view.edit_action = self.view.view_selected
        self.centrallayout.addWidget(self.view)

        add_action = QtWidgets.QAction(QtGui.QIcon.fromTheme("list-add"), "Add", self)
        add_action.setShortcut("Ctrl+A")
        add_action.triggered.connect(self.add_note)
        self.toolbar.addAction(add_action)

        remove_action = QtWidgets.QAction(QtGui.QIcon.fromTheme("list-remove"), "Remove", self)
        remove_action.setShortcut("Ctrl+R")
        remove_action.triggered.connect(self.remove_note)
        self.toolbar.addAction(remove_action)

        unlock_action = source_unlock_dialog.UnlockAction(model.source, self)
        unlock_action.setShortcut("Ctrl+U")
        self.toolbar.addAction(unlock_action)

    def add_note(self):
        note = potash.builtin_objects.Note(self.view.model().source)
        if not object_edit_widget.ObjectEditDialog.edit([note],
                                                        [object_model.ObjectModelHeader("summary"),
                                                         object_model.ObjectModelHeader("tags"),
                                                         object_model.ObjectModelHeader("description")], self):
            note.destroy()

    def remove_note(self):
        for obj in self.view.selectedObjects():
            obj.destroy()
        self.view.model().source.commit()
