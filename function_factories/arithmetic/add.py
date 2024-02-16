from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Add(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Add"

    def _init_parameters(self) -> List[Parameter]:
        constraint = Constraints(0., 1., 0.001, float)
        per_channel = NumberParameter("Per channel",
                                      "per_channel",
                                      0,
                                      constraint)
        constraint = Constraints(-255, 255, 1, int)
        string_lower = StringDescription("from: ")
        string_upper = StringDescription("to: ")
        low_end_param = NumberParameter("Low end",
                                        "low_end",
                                        -20,
                                        constraint)
        high_end_param = NumberParameter("High end",
                                         "high_end",
                                         20,
                                         constraint)
        shift_x_percentage = TupleParameter("Value to add",
                                             "value",
                                            (string_lower,
                                             low_end_param,
                                             string_upper,
                                             high_end_param))

        return [shift_x_percentage, per_channel]

    def _init_function(self) -> callable:
        return iaa.Add

    def _init_sub_functions_param(self) -> str:
        return ""
