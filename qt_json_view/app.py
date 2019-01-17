#! /bin/env python


if __name__ == '__main__':
    import sys    
    import json

    from Qt import QtWidgets
    from qt_json_view.view import JsonView
    from qt_json_view.model import JsonModel

    class App(QtWidgets.QApplication):
        data = {
            "none": None,
            "bool": True,
            "int": 666,
            "float": 1.23,
            "list": [1, 2, 3],
            "empty_list": [],
            "dict": {"key": "value"},
            "nested_dict": {
                "dict": {
                    "key": "value",
                    "empty_list": []}}}

        def __init__(self, sys_argv):
            super(App, self).__init__(sys_argv)

            self.widget = widget = QtWidgets.QWidget()
            widget.setLayout(QtWidgets.QVBoxLayout())
            widget.setGeometry(100, 100, 400, 400)

            button = QtWidgets.QPushButton("Serialize")

            self.view = view = JsonView()
            self.model = model = JsonModel()

            widget.layout().addWidget(view)
            widget.layout().addWidget(button)

            model.items_from_dict(data=self.data)
            view.setModel(model)

            button.clicked.connect(self.serialize)

        def serialize(self):
            print(json.dumps(self.model.serialize(), indent=2))


    app = App(sys.argv)
    app.widget.show()
    app.view.expandAll()
    sys.exit(app.exec_())
