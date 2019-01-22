#! /bin/env python
import json
import tempfile

from Qt import QtWidgets, QtCore
from qt_json_view.view import JsonView
from qt_json_view.model import JsonModel
from qt_json_view.utils import load, dump


def dumpTestData(encoding="json"):
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

    result = tempfile.mkstemp(suffix="." + encoding)
    dump(data, result[-1], encoding=encoding)

    return result[-1]


def loadTestData(filepath, encoding="json"):
    return load(filepath, encoding=encoding)


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
        button.clicked.connect(self.serialize)

        # TODO: Pickle error
        button = QtWidgets.QPushButton("&Save")
        self.vboxlayout.addWidget(button)
        button.clicked.connect(self.onSaveClicked)

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

    def serialize(self):
        tmp = tempfile.mkstemp(suffix=".json")[-1]
        print(json.dumps(self.view.model().serialize(), indent=2))
        dump(json.dumps(self.view.model().serialize()), tmp, encoding="json")
        self.statusBar().showMessage("File saved: {}".format(tmp))

    def onSaveClicked(self):
        tmp = tempfile.mkstemp(suffix=".json")[-1]
        file = QtCore.QFile(tmp)
        file.open(QtCore.QIODevice.WriteOnly)
        stream = QtCore.QDataStream(file)
        model = self.view.model()
        self.saveModel(model.invisibleRootItem(), stream)
        file.close()
        self.statusBar().showMessage("File saved: {}".format(tmp))

    def saveModel(self, item, stream):
        for i in range(0, item.rowCount()):
            child = item.child(i)
            child.write(stream)
            self.saveModel(child, stream)

