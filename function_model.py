from copy import deepcopy
from typing import List

from PySide6.QtCore import Property, QObject, Slot

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

    # TODO: serialization, save just the values not everyhing
    def to_dict(self):
        return {
            "name": self._name,
            "parameters": [p.to_dict() for p in self._parameters],
            "sub_functions_param": self._sub_functions_param,
        }

    @staticmethod
    def from_dict(d):
        name = d["name"]
        parameters = [Parameter.from_dict(p) for p in d["parameters"]]
        sub_functions_param = d["sub_functions_param"]

        from function_database import FunctionDatabase
        function = FunctionDatabase.get_function_by_name(name)
        return FunctionModel(name, parameters, function, sub_functions_param)


    @Property(str, constant=True)
    def name(self):
        return self._name

    # todo: parameters might have varying constraints based on circumstances
    @Property('QVariantList', constant=True)
    def parameters(self):
        return self._parameters

    @Slot(result=bool)
    def expects_sub_functions(self):
        return self._sub_functions_param != ""

    def get_function_lambda(self, sub_functions: List[callable] = None) -> callable:
        parameters_dict = {p.parameter_name: p.value for p in self._parameters}
        if sub_functions is not None:
            parameters_dict[self._sub_functions_param] = [f() for f in sub_functions]
        return lambda: self._function(**parameters_dict)

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

    @property
    def function(self):
        return self._function

    @Slot(bool, result=FunctionModel)
    def get_function_model(self, from_qml=False):
        function_model = FunctionModel(self._name,
                                       [parameter.deepcopy() for parameter in self._parameters],
                                       self._function,
                                       self._sub_functions_param,
                                       self if from_qml else None)
        return function_model
