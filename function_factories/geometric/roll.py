from typing import List

from projects_src.augmentation_gui.custom_functions.roll import RollAugment
from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Roll(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Roll"

    def _init_parameters(self) -> List[Parameter]:
        constraint = Constraints(-1., 1., 0.01, float)
        string_lower = StringDescription("from: ")
        string_upper = StringDescription("to: ")
        low_end_param = NumberParameter("Low end",
                                        "low_end",
                                        -0.5,
                                        constraint)
        high_end_param = NumberParameter("High end",
                                         "high_end",
                                         0.5,
                                         constraint)
        shift_x_percentage = TupleParameter("Roll ratio x",
                                             "roll_x_ratio",
                                            (string_lower,
                                             low_end_param.deepcopy(),
                                             string_upper,
                                             high_end_param.deepcopy()))

        shift_y_percentage = TupleParameter("Roll ratio y",
                                             "roll_y_ratio",
                                            (string_lower,
                                             low_end_param.deepcopy(),
                                             string_upper,
                                             high_end_param.deepcopy()))
        return [shift_x_percentage, shift_y_percentage]

    def _init_function(self) -> callable:
        return RollAugment

    def _init_sub_functions_param(self) -> str:
        return ""
