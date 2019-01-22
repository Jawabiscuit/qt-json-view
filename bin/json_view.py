#! /usr/bin/env python
from qt_json_view.app import MainWindow, dumpTestData, loadTestData


if __name__ == "__main__":
    import sys
    from Qt.QtWidgets import QApplication
    
    app = QApplication(sys.argv)

    fp = dumpTestData()
    data = loadTestData(fp)

    ui = MainWindow(data)
    ui.show()

    sys.exit(app.exec_())
