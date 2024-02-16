from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class AddElementwise(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Add Elementwise"

    def _init_parameters(self) -> List[Parameter]:
        constraint = Constraints(-255, 255, 1, int)
        value_from = NumberParameter("from",
                                     "value",
                                     -20,
                                     constraint)
        value_to = NumberParameter("to",
                                   "value",
                                   20,
                                   constraint)
        string_lower = StringDescription("from: ")
        string_upper = StringDescription("to: ")

        value = TupleParameter("Value",
                               "value",
                               (string_lower,
                                value_from,
                                string_upper,
                                value_to))

        constraint_per_channel = Constraints(0., 1., 0.01, float)
        per_channel = NumberParameter("Per channel",
                                      "per_channel",
                                      0.,
                                      constraint_per_channel)

        return [value, per_channel]

    def _init_function(self) -> callable:
        return iaa.AddElementwise

    def _init_sub_functions_param(self) -> str:
        return ""
