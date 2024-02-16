from __future__ import annotations

import pickle

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex, QObject, Property, Slot, Signal
from PySide6.QtGui import QStandardItem

from function_factories.meta.sequential import Sequential
from function_factories.empty import Empty
from function_model import FunctionModel


class FunctionModelItem:
    def __init__(self,
                 fnc_model: FunctionModel,
                 parent=None):
        self.parentItem = parent
        self.fnc_model = fnc_model
        self.child_items = []

    def to_dict(self):
        return {
            "fnc_model": self.fnc_model.to_dict(),
            "child_items": [child.to_dict() for child in self.child_items]
        }

    @staticmethod
    def from_dict(d, parent=None) -> FunctionModelItem:
        f_model = FunctionModel.from_dict(d["fnc_model"])
        item = FunctionModelItem(f_model, parent)
        item.child_items = [FunctionModelItem.from_dict(child, item) for child in d["child_items"]]
        return item

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

    def removeChild(self, position):
        self.child_items.pop(position)

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

    def build_callable_pipeline(self):
        if self.fnc_model.expects_sub_functions():
            sub_functions = [child.build_callable_pipeline() for child in self.child_items]
            return self.fnc_model.get_function_lambda(sub_functions)
        else:
            return self.fnc_model.get_function_lambda()


class TreeModel(QAbstractItemModel):
    activeFunctionChanged = Signal()

    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = FunctionModelItem(Sequential().get_function_model())
        self._empty_item = FunctionModelItem(Empty().get_function_model())
        self.rootItem.appendChild(self._empty_item)
        self._active_function = self._empty_item.fnc_model

    def to_dict(self):
        return self.rootItem.to_dict()

    def from_dict(self, d):
        self.beginResetModel()
        self.rootItem = FunctionModelItem.from_dict(d)
        self._activeFunction = self.rootItem.fnc_model
        self.endResetModel()

    def reset_model(self):
        self.beginResetModel()
        self.rootItem = FunctionModelItem(Sequential().get_function_model())
        self.endResetModel()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.rootItem.appendChild(self._empty_item)
        self.active_function = self._empty_item.fnc_model
        self.endInsertRows()

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

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

    @Slot(QModelIndex, result=None)
    def setActiveFunction(self, index: QModelIndex):
        self.activeFunction = index.internalPointer().fnc_model

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

        if self.rootItem.child_items[0] is self._empty_item:
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self.rootItem.removeChild(0)
            self.endRemoveRows()

        return True

    @Slot(QModelIndex, result=bool)
    def removeItemAtIndex(self, index: QModelIndex):
        if not index.isValid():
            return False
        item = index.internalPointer()
        parent_index = self.parent(index)
        self.beginRemoveRows(parent_index, item.row(), item.row())
        if self._active_function is item.fnc_model:
            self.activeFunction = self.rootItem.fnc_model
        item.parent().removeChild(item.row())

        self.endRemoveRows()

        if self.rootItem.childCount() == 0:
            self.reset_model()

    @Property(FunctionModel, notify=activeFunctionChanged)
    def activeFunction(self) -> FunctionModel:
        return self._active_function

    @activeFunction.setter
    def activeFunction(self, value: FunctionModel):
        if self._active_function != value:
            self._active_function = value
            self.activeFunctionChanged.emit()

    def build_callable_pipeline(self):
        return self.rootItem.build_callable_pipeline()()
