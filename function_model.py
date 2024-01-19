from typing import List

from PySide6.QtCore import Property, QObject, Slot
from PySide6.QtQml import QQmlEngine

from parameter_models.parameter_interface import Parameter


class FunctionModel(QObject):
    def __init__(self,
                 name: str,
                 parameters: list,
                 function: callable,
                 sub_functions_param: str = "",
                 parent=None):
        super().__init__(parent)
        self._name = name
        self._parameters = parameters
        self._sub_functions_param = sub_functions_param
        self._function = function

    @Property(str, constant=True)
    def name(self):
        return self._name

    @Property('QVariantList', constant=True)
    def parameters(self):
        return self._parameters

    @Slot(result=bool)
    def expects_sub_functions(self):
        return self._sub_functions_param != ""

    def get_function_lambda(self):
        return lambda: self._function(**{p.name: p.value for p in self._parameters})

    def __repr__(self):
        return f"{self._name}: {self._parameters}"

    def __str__(self):
        return f"{self._name}: {self._parameters}"


class IFunctionFactory(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = self._init_name()
        self._parameters = self._init_parameters()
        self._function = self._init_function()
        self._sub_functions_param = self._init_sub_functions_param()

    def _init_name(self) -> str:
        raise NotImplementedError

    def _init_parameters(self) -> List[Parameter]:
        raise NotImplementedError

    def _init_function(self) -> callable:
        raise NotImplementedError

    def _init_sub_functions_param(self) -> str:
        raise NotImplementedError

    @Property(str, constant=True)
    def name(self):
        return self._name

    @Slot(bool, result=FunctionModel)
    def get_function_model(self, from_qml=False):
        function_model = FunctionModel(self._name,
                                       self._parameters,
                                       self._function,
                                       self._sub_functions_param,
                                       self if from_qml else None)
        return function_model
