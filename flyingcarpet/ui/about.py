from PyQt5 import QtCore, QtGui, QtWidgets

from ..build import FileBuilder


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.setModal(True)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.setWindowTitle("About")

        data = app.app_data()
        self.table_widget = QtWidgets.QTableWidget(len(data), 2, self)
        for row, (name, value) in enumerate(data):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(value))
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.verticalHeader().setStretchLastSection(True)
        self.layout().addWidget(self.table_widget)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, self)
        self.layout().addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @classmethod
    def about(cls, app, parent=None):
        dialog = cls(app, parent)
        return dialog.exec_()
