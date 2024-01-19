from typing import List

from PySide6.QtCore import Property, Slot
from imgaug import augmenters as iaa

from function_model import FunctionModel, IFunctionFactory
from parameter_models.constraints import Constraints
from parameter_models.number_parameter import NumberParameter
from parameter_models.parameter_interface import Parameter


class TranslateX(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Translate X"

    def _init_parameters(self) -> List[Parameter]:
        shift_x_percentage = NumberParameter("Shift in percentage",
                                             0.5,
                                             Constraints(0.,
                                                         1.,
                                                         0.01,
                                                         float))
        return [shift_x_percentage]

    def _init_function(self) -> callable:
        return iaa.TranslateX

    def _init_sub_functions_param(self) -> str:
        return ""

    @Property(str, constant=True)
    def name(self):
        return self._name


class Sequential(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Sequential"

    def _init_parameters(self) -> List[Parameter]:
        return []

    def _init_function(self) -> callable:
        return iaa.Sequential

    def _init_sub_functions_param(self) -> str:
        return "children"

    @Property(str, constant=True)
    def name(self):
        return self._name


class FunctionDatabase:
    function_database = [TranslateX(),
                         Sequential()]

    @staticmethod
    def __iter__():
        return iter(FunctionDatabase.function_database)

    # function_database = [FunctionModel("Translate x",
    #                                    [
    #                                        BooleanParameter("percent", False),
    #                                        NumberParameter("percent",
    #                                                        1,
    #                                                        Constraints(0., 2., 0.01, float)),
    #                                        NumberParameter("percent",
    #                                                        1,
    #                                                        Constraints(0., 4., 0.01, float)),
    #                                        TupleParameter("kernel", fields_tuple=(StringDescription("k1"),
    #                                                                               NumberParameter("k1",
    #                                                                                               1,
    #                                                                                               Constraints(1, 99999,
    #                                                                                                           1, int)),
    #                                                                               StringDescription("k2"),
    #                                                                               NumberParameter("k2",
    #                                                                                               1,
    #                                                                                               Constraints(1, 99999,
    #                                                                                                           1, int)),)
    #                                                       )
    #                                    ],
    #                                    iaa.TranslateX,
    #                                    "",),
    #                      FunctionModel("Translate y",
    #                                    [NumberParameter("percent",
    #                                                     0,
    #                                                     Constraints(0., 1., 0.01, float))],
    #
    #                                    iaa.TranslateY,
    #                      "",)]
