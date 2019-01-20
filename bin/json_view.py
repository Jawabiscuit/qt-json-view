#! /usr/bin/env python
from qt_json_view.app import App


if __name__ == "__main__":
    import sys
    app = App(sys.argv)
    app.widget.show()
    app.view.expandAll()
    sys.exit(app.exec_())
