# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, Signal, Property
from PySide6.QtGui import QGuiApplication, QFontDatabase, QStandardItem, QStandardItemModel
from PySide6.QtQml import qmlRegisterType, QQmlApplicationEngine

from function_database import FunctionDatabase, TranslateX, Sequential
from function_model_tree import TreeModel, FunctionModelItem


class FunctionSet:
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions


class MyModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._augmentationString = ""

    # Signal that is emitted when the titleString property changes
    augmentationStringChanged = Signal()

    @Property(str, notify=augmentationStringChanged)
    def augmentationString(self):
        return self._augmentationString

    @augmentationString.setter
    def augmentationString(self, value):
        if self._augmentationString != value:
            self._augmentationString = value
            self.augmentationStringChanged.emit()


if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.addImportPath(str(Path(__file__).resolve().parent))
    engine.addImportPath(QCoreApplication.applicationDirPath() + "/qml")
    engine.addImportPath(QCoreApplication.applicationDirPath() + ":/content")
    engine.addImportPath(":/")
    content_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'content')
    engine.addImportPath(content_dir)
    imports_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imports')
    engine.addImportPath(imports_dir)

    font_database = QFontDatabase()
    font_database.addApplicationFont(":/content/fonts/fonts.txt")
    function_set = FunctionSet("My Functions", ["Function 1", "Function 2", "Function 3"])

    # Add the function set to the model
    item = QStandardItem(function_set.name)
    for function in function_set.functions:
        tmp_item = QStandardItem(function)
        tmp_item.appendRow(QStandardItem("Sub Function 1"))
        item.appendRow(tmp_item)


    model = QStandardItemModel()
    model.appendRow(item)

    tree_model = TreeModel()
    tree_model.rootItem.appendChild(FunctionModelItem(TranslateX().get_function_model(), tree_model.rootItem))
    item = FunctionModelItem(Sequential().get_function_model(), tree_model.rootItem)
    item.appendChild(FunctionModelItem(TranslateX().get_function_model(), item))
    item.appendChild(FunctionModelItem(TranslateX().get_function_model(), item))
    tree_model.rootItem.appendChild(item)
    # Call the index method
    index = tree_model.index(0, 0)

    # Print the returned QModelIndex
    print(tree_model.rowCount())
    engine.rootContext().setContextProperty("myModel", tree_model)
    model2 = MyModel()
    engine.rootContext().setContextProperty("augmentationTitleTextModel", model2)
    model2.augmentationString = "Augmentation"
    qml_file = Path(__file__).resolve().parent / "main.qml"
    model2.augmentationString = "pen"

    engine.rootContext().setContextProperty("functionDatabase", FunctionDatabase.function_database)

    item = QStandardItem("function_set.name")
    item2 = QStandardItem("Function 1")
    item3 = QStandardItem("Function 1")

    model3 = QStandardItemModel()
    model3.appendRow(item)
    model3.appendRow(item2)
    model3.appendRow(item3)
    instantiated_function = FunctionDatabase.function_database[0].get_function_model()
    engine.rootContext().setContextProperty("functionModel", instantiated_function)

    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
