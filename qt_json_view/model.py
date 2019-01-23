"""
TODO _item_changed()
"""
from Qt import QtCore, QtGui, QtWidgets


class JsonModel(QtGui.QStandardItemModel):
    """Model representing a JSON-serializable dictionary."""

    def __init__(self, parent=None):
        super(JsonModel, self).__init__(parent=parent)
        self.setHorizontalHeaderLabels(["Key", "Value"])
        self.itemChanged.connect(self._item_changed)

    @QtCore.Slot(QtGui.QStandardItem)
    def _item_changed(self, item):
        """TODO"""
        print("_item_changed", item)
        print("row:", item.index().row())
        print("col:", item.index().column())
        print("data:", item.data(QtCore.Qt.DisplayRole))
        print("data:", item.data(QtCore.Qt.UserRole))
        print("col count:", self.columnCount())
        key_item = self.item(item.index().row(), 0)
        print("k_row:", key_item.index().row())
        print("k_col:", key_item.index().column())
        print("data:", key_item.data(QtCore.Qt.DisplayRole))
        print("data:", key_item.data(QtCore.Qt.UserRole))
        
        row = item.index().row()
        parent = item.parent()
        if parent is None:
            parent = self.invisibleRootItem()

        if item.index().column() > 0:
            print("poo")
            key_item = self.item(row, 0)
            data_type = key_item.data(QtCore.Qt.UserRole)

            if data_type is list:
                #parent = item

                try:
                    data = eval(item.data(QtCore.Qt.DisplayRole))
                except:
                    import traceback
                    traceback.print_exc()
                    return
                else:
                    print("data", data)
                    print("parent", parent.text())
                    # self.items_from_list(data, parent)

                self.takeRow(row)
                print("k_item:", key_item.text())
                empty_item = self._create_empty_item()
                parent.insertRow(row, [key_item, empty_item])

                parent = key_item
                for i, value in enumerate(data):
                    value_item = self._create_value_item(value)
                    key_item = self._create_key_item(str(i), data_type=type(value))
                    parent.appendRow([key_item, value_item])

    def items_from_dict(self, data, parent=None):
        """Represent the dictionary by items."""
        if parent is None:
            parent = self.invisibleRootItem()
        for key, value in data.items():
            key_item = self._create_key_item(key, data_type=type(value))
            empty_item = self._create_empty_item()
            if isinstance(value, dict):
                # insert {} display values for empty dicts
                if value == {}:
                    value_item = self._create_value_item(value)
                    parent.appendRow([key_item, value_item])
                else:
                    parent.appendRow([key_item, empty_item])
                    self.items_from_dict(value, key_item)
            elif isinstance(value, list):
                # insert [] display values for empty lists
                if value == []:
                    value_item = self._create_value_item(value)
                    parent.appendRow([key_item, value_item])
                else:
                    parent.appendRow([key_item, empty_item])
                    self.items_from_list(value, key_item)
            else:
                value_item = self._create_value_item(value)
                parent.appendRow([key_item, value_item])

    def items_from_list(self, data, parent):
        """Represent the list by items."""
        for i, value in enumerate(data):
            key_item = self._create_key_item(str(i), data_type=type(value))
            empty_item = self._create_empty_item()
            if isinstance(value, dict):
                # insert {} display values for empty dicts
                if value == {}:
                    value_item = self._create_value_item(value)
                    parent.appendRow([key_item, value_item])
                else:
                    parent.appendRow([key_item, empty_item])
                    self.items_from_dict(value, key_item)
            elif isinstance(value, list):
                # insert [] display values for empty lists
                if value == []:
                    value_item = self._create_value_item(value)
                    parent.appendRow([key_item, value_item])
                else:
                    parent.appendRow([key_item, empty_item])
                    self.items_from_list(value, key_item)
            else:
                value_item = self._create_value_item(value)
                parent.appendRow([key_item, value_item])

    def _create_key_item(self, key, data_type=None):
        """Item representing a key."""
        key_item = QtGui.QStandardItem(key)
        key_item.setData(data_type, QtCore.Qt.UserRole)
        key_item.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsEditable)
        return key_item

    def _get_display_value(self, value):
        """Get an items representation"""
        return ("null" if value is None
                else "[]" if value == []
                else "{}" if value == {}
                else "\"\"" if value == ""
                else str(value))

    def _create_value_item(self, value):
        """Item representing a value."""
        display_value = self._get_display_value(value)
        value_item = QtGui.QStandardItem(display_value)
        value_item.setData(display_value, QtCore.Qt.DisplayRole)
        value_item.setData(value, QtCore.Qt.UserRole)
        flags = QtCore.Qt.ItemIsSelectable
        if isinstance(value, bool):
            flags |= (QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsUserCheckable)
            value_item.setCheckState(
                QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
            value_item.setData("", QtCore.Qt.DisplayRole)
        else:
            flags |= QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        value_item.setFlags(flags)
        return value_item

    # def _create_add_item(self, parent):
    #     add_item = QtGui.QStandardItem("__add_item__")
    #     add_item.setFlags(
    #         QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    #     empty_item = QtGui.QStandardItem()
    #     empty_item.setFlags(QtCore.Qt.ItemIsEnabled)
    #     parent.appendRow([add_item, empty_item])

    def _create_empty_item(self):
        empty_item = QtGui.QStandardItem()
        empty_item.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return empty_item

    def serialize(self):
        """Assemble the model back into a dictionary.

        The return dictionary is based on the original dictionary.
        """
        data = {}
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            key = item.data(QtCore.Qt.DisplayRole)
            # if item.data(QtCore.Qt.DisplayRole) == "__add_item__":
                # continue
            data[key] = self._serialize(item)
        return data

    def _serialize(self, item):
        """Create a dictionary from the model items."""
        data_type = item.data(QtCore.Qt.UserRole)
        if data_type == dict:
            serialized = {}
        elif data_type == list:
            serialized = []
        else:
            parent = item.parent()
            if parent is None:
                parent = self.invisibleRootItem()
            serialized = self._value(parent, item.row())
        for row in range(item.rowCount()):
            key = item.child(row, 0).data(QtCore.Qt.DisplayRole)
            value = self._value(item, row)
            # if item.child(row, 0).data(QtCore.Qt.DisplayRole) == "__add_item__":
                # continue
            if data_type == dict:
                serialized[key] = value
            elif data_type == list:
                serialized.append(value)
        return serialized

    def _value(self, item, row):
        key_child = item.child(row, 0)
        if (key_child.data(QtCore.Qt.UserRole) == dict or
                key_child.data(QtCore.Qt.UserRole) == list):
            value = self._serialize(key_child)
        else:
            value_child = item.child(row, 1)
            value = value_child.data(QtCore.Qt.DisplayRole)
            user_value = value_child.data(QtCore.Qt.UserRole)
            if value_child.isCheckable():
                value = (True if item.child(row, 1).checkState() ==
                         QtCore.Qt.Checked else False)
            if user_value is None and value == "None":
                value = user_value
        return value
