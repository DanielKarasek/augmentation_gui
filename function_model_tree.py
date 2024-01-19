from __future__ import annotations
from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, QObject, Property, Slot
from PySide6.QtGui import QStandardItem

from function_database import Sequential
from function_model import FunctionModel


class FunctionModelItem:
    def __init__(self,
                 fnc_model: FunctionModel,
                 parent=None):
        self.parentItem = parent
        self.fnc_model = fnc_model
        self.child_items = []

    def appendChild(self, item: FunctionModelItem):
        item.parentItem = self
        if self.fnc_model.expects_sub_functions():
            self.child_items.append(item)
        else:
            raise ValueError(f"Function {self.fnc_model.name} doesn't expect subfunctions")

    def insertChild(self, position, item: FunctionModelItem):
        item.parentItem = self
        if self.fnc_model.expects_sub_functions():
            self.child_items.insert(position, item)
        else:
            raise ValueError(f"Function {self.fnc_model.name} doesn't expect subfunctions")

    def child(self, row):
        return self.child_items[row]

    def childCount(self):
        return len(self.child_items)

    def columnCount(self):
        return 1

    def data(self, column):
        if column == 0:
            return self.fnc_model
        else:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.child_items.index(self)
        return 0



class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = FunctionModelItem(Sequential().get_function_model())

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return index.data().name

        item = index.internalPointer()
        return item.data(index.column())

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "Function"
        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    @Slot(int, result=QModelIndex)
    def getIndex(self, currentIndex: int) -> QModelIndex:
        stack = [(child,
                  self.createIndex(self.rootItem.row(), 0, child))
                 for child in self.rootItem.child_items]
        currentRow = 0
        while stack:
            item, parentIndex = stack.pop(0)
            if currentRow == currentIndex:
                return self.createIndex(item.row(), 0, item)
            currentRow += 1
            stack = [(child, self.createIndex(item.row(), 0, item)) for child in item.child_items] + stack

        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    @Slot(QModelIndex, FunctionModel, bool, result=bool)
    def addItemAtIndex(self, index: QModelIndex, fnc_model: FunctionModel, as_child: bool = True):
        if not index.isValid():
            return False

        item = index.internalPointer()
        new_item = FunctionModelItem(fnc_model)

        if as_child:
            self.beginInsertRows(index, item.childCount(), item.childCount())
            item.appendChild(new_item)
            self.endInsertRows()
        else:
            parent_index = self.parent(index)
            position = item.row() + 1
            self.beginInsertRows(parent_index, position, position)
            item.parent().insertChild(position, new_item)
            self.endInsertRows()

        return True