#! /bin/env python
import json
import tempfile

from Qt import QtWidgets, QtCore
from qt_json_view.view import JsonView
from qt_json_view.model import JsonModel
from qt_json_view.utils import load, dump


def dumpTestData(format="json"):
    data = {
        "none": None,
        "bool": True,
        "int": 666,
        "float": 1.23,
        "list": [1, 2, 3],
        "empty_list": [],
        "dict": {"key": "value"},
        "empty_dict": {},
        "nested_dict": {
            "dict": {
                "key": "value",
                "empty_list": []},
            "empty_dict": {},}}

    result = tempfile.mkstemp(suffix="." + format)
    dump(data, result[-1], format=format)

    return result[-1]


def loadTestData(filepath, format="json"):
    return load(filepath, format=format)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, parent=None):
        super(MainWindow, self).__init__()
        self.resize(250, 400)

        self.setCentralWidget(QtWidgets.QWidget())

        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralWidget())
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        
        self.view = JsonView()
        self.vboxlayout.addWidget(self.view)

        model = JsonModel()
        model.items_from_dict(data=data)
        self.view.setModel(model)

        self.view.expandAll()
        for column in range(model.columnCount()):
            self.view.resizeColumnToContents(column)

        button = QtWidgets.QPushButton("Serialize")
        self.vboxlayout.addWidget(button)
        button.clicked.connect(self.onSerializePressed)

        # TODO: Pickle error
        # button = QtWidgets.QPushButton("&Save")
        # self.vboxlayout.addWidget(button)
        # button.clicked.connect(self.onSavePressed)

        button = QtWidgets.QPushButton("Load")
        self.vboxlayout.addWidget(button)
        button.clicked.connect(self.onLoadPressed)

        selectionModel = self.view.selectionModel()
        self.view.selectionModel().selectionChanged.connect(
            self.selectionChanged)

    def selectionChanged(self, *args, **kwargs):
        hasCurrent = self.view.selectionModel().currentIndex().isValid()
        if hasCurrent:
            currentIndex = self.view.selectionModel().currentIndex()
            
            # TODO: What exactly does this do?
            self.view.closePersistentEditor(currentIndex)
            
            row = currentIndex.row()
            col = currentIndex.column()
            parent = currentIndex.parent()

            if parent.isValid():
                self.statusBar().showMessage("Pos: ({}, {})".format(row, col))
            else:
                self.statusBar().showMessage("Pos: ({}, {}) in top level".format(row, col))

    @QtCore.Slot()
    def onSerializePressed(self):
        tmp = tempfile.mkstemp(suffix=".json")[-1]
        print(json.dumps(self.view.model().serialize(), indent=2))
        dump(self.view.model().serialize(), tmp, format="json", indent=2)
        self.statusBar().showMessage("File saved: {}".format(tmp))

    @QtCore.Slot()
    def onSavePressed(self):
        tmp = tempfile.mkstemp(suffix=".json")[-1]
        file = QtCore.QFile(tmp)
        file.open(QtCore.QIODevice.WriteOnly)
        stream = QtCore.QDataStream(file)
        model = self.view.model()
        self.saveModel(model.invisibleRootItem(), stream)
        file.close()
        self.statusBar().showMessage("File saved: {}".format(tmp))

    @QtCore.Slot()
    def onLoadPressed(self):
        fileName = self.setOpenFileName()
        if not fileName:
            return
        data = load(fileName, format="json")

        from pprint import pprint
        pprint(data)

        if data:
            model = JsonModel()
            model.items_from_dict(data=data)
            self.view.setModel(model)

    def setOpenFileName(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Text Files (*.txt)", "", options)
        if fileName:
            self.statusBar().showMessage("Loading file: {}".format(fileName))
        return fileName

    def saveModel(self, item, stream):
        for i in range(0, item.rowCount()):
            child = item.child(i)
            child.write(stream)
            self.saveModel(child, stream)

